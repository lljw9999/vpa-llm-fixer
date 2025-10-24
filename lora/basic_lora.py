#!/usr/bin/env python3
"""Minimal LoRA fine-tuning script for Qwen 2.5 Instruct."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import torch
from datasets import Dataset, DatasetDict, load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    set_seed,
)
from trl import DataCollatorForCompletionOnlyLM, SFTTrainer


DEFAULT_TARGET_MODULES: Iterable[str] = (
    "q_proj",
    "k_proj",
    "v_proj",
    "o_proj",
    "gate_proj",
    "up_proj",
    "down_proj",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run supervised fine-tuning on Qwen 2.5 Instruct with LoRA adapters.",
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Hugging Face dataset name/path or local file directory containing a 'train' split.",
    )
    parser.add_argument(
        "--model-name",
        default="Qwen/Qwen2.5-7B-Instruct",
        help="Base model repository id or local path.",
    )
    parser.add_argument(
        "--output-dir",
        default="qwen2.5-lora",
        help="Directory where checkpoints and adapters are stored.",
    )
    parser.add_argument(
        "--num-train-epochs",
        type=float,
        default=3.0,
        help="Total training epochs.",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=2e-4,
        help="Peak learning rate for the LoRA parameters.",
    )
    parser.add_argument(
        "--per-device-train-batch-size",
        type=int,
        default=1,
        help="Batch size per device for training.",
    )
    parser.add_argument(
        "--gradient-accumulation-steps",
        type=int,
        default=16,
        help="Accumulate gradients to simulate a larger batch.",
    )
    parser.add_argument(
        "--warmup-ratio",
        type=float,
        default=0.1,
        help="Warmup ratio for the scheduler.",
    )
    parser.add_argument(
        "--eval-split",
        type=float,
        default=0.05,
        help="If no validation split is provided, reserve this fraction from train for evaluation.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--max-seq-length",
        type=int,
        default=4096,
        help="Maximum sequence length when packing samples.",
    )
    parser.add_argument(
        "--packing",
        action="store_true",
        help="Enable TRL packing to combine shorter examples in the same sequence.",
    )
    parser.add_argument(
        "--gradient-checkpointing",
        action="store_true",
        help="Enable gradient checkpointing to trade compute for memory.",
    )
    parser.add_argument(
        "--resume-from-checkpoint",
        default=None,
        help="Checkpoint directory to resume training from.",
    )
    parser.add_argument(
        "--merge-and-unload",
        action="store_true",
        help="Merge LoRA adapters into the base model after training finishes.",
    )
    parser.add_argument(
        "--target-modules",
        nargs="+",
        default=list(DEFAULT_TARGET_MODULES),
        help="Transformer modules to wrap with LoRA adapters.",
    )
    return parser.parse_args()


def detect_bf16_support() -> bool:
    if not torch.cuda.is_available():
        return False
    major, _ = torch.cuda.get_device_capability(0)
    return major >= 8


def prepare_datasets(
    dataset_id: str,
    tokenizer,
    eval_split: float,
) -> tuple:
    raw_dataset = load_dataset(dataset_id)

    if isinstance(raw_dataset, Dataset):
        raw_dataset = DatasetDict({"train": raw_dataset})

    if "train" not in raw_dataset:
        raise ValueError("Dataset must contain a 'train' split.")

    if "validation" not in raw_dataset:
        split_dataset = raw_dataset["train"].train_test_split(test_size=eval_split, seed=42)
        raw_dataset["train"] = split_dataset["train"]
        raw_dataset["validation"] = split_dataset["test"]

    def convert_to_text(example):
        messages = example["messages"]
        if not isinstance(messages, list):
            raise ValueError("Each example must expose a 'messages' list of chat turns.")
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False,
        )
        return {"text": text}

    column_names = raw_dataset["train"].column_names
    train_dataset = raw_dataset["train"].map(
        convert_to_text,
        remove_columns=column_names,
    )
    eval_dataset = raw_dataset["validation"].map(
        convert_to_text,
        remove_columns=raw_dataset["validation"].column_names,
    )

    return train_dataset, eval_dataset


def build_model(
    model_name: str,
    target_modules: Iterable[str],
    gradient_checkpointing: bool,
) -> torch.nn.Module:
    torch_dtype = torch.bfloat16 if detect_bf16_support() else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        load_in_4bit=True,
        device_map="auto",
        torch_dtype=torch_dtype,
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)

    if gradient_checkpointing:
        model.gradient_checkpointing_enable()
        model.config.use_cache = False

    lora_config = LoraConfig(
        r=64,
        lora_alpha=16,
        target_modules=list(target_modules),
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    peft_model = get_peft_model(model, lora_config)
    peft_model.print_trainable_parameters()
    return peft_model


def main() -> None:
    args = parse_args()

    set_seed(args.seed)

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name,
        trust_remote_code=True,
        padding_side="right",
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    train_dataset, eval_dataset = prepare_datasets(
        dataset_id=args.dataset,
        tokenizer=tokenizer,
        eval_split=args.eval_split,
    )

    collator = DataCollatorForCompletionOnlyLM(
        response_template="<|im_start|>assistant\n",
        tokenizer=tokenizer,
        pad_to_multiple_of=8 if torch.cuda.is_available() else None,
    )

    model = build_model(
        model_name=args.model_name,
        target_modules=args.target_modules,
        gradient_checkpointing=args.gradient_checkpointing,
    )

    supports_bf16 = detect_bf16_support()

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        lr_scheduler_type="cosine",
        warmup_ratio=args.warmup_ratio,
        logging_steps=10,
        evaluation_strategy="steps",
        eval_steps=200,
        save_steps=200,
        save_total_limit=2,
        bf16=supports_bf16,
        gradient_checkpointing=args.gradient_checkpointing,
        report_to=["tensorboard"],
        optim="paged_adamw_32bit",
        max_grad_norm=1.0,
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=collator,
        args=training_args,
        max_seq_length=args.max_seq_length,
        packing=args.packing,
    )

    trainer.train(resume_from_checkpoint=args.resume_from_checkpoint)

    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    if args.merge_and_unload:
        merged_dir = Path(args.output_dir) / "merged"
        merged_dir.mkdir(parents=True, exist_ok=True)
        merged_model = model.merge_and_unload()
        merged_model.save_pretrained(merged_dir)
        tokenizer.save_pretrained(merged_dir)


if __name__ == "__main__":
    main()
