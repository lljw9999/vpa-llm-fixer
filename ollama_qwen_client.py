#!/usr/bin/env python3
"""Minimal client for talking to a local Ollama Qwen3 1.7B model.

The script sends chat-style prompts to the Ollama REST API.  By default it
targets a local daemon (`http://localhost:11434`) and the `qwen3:1.7b` model,
but both can be overridden with CLI flags or environment variables.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Iterator, Optional
import json

try:
    import requests
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "This script requires the `requests` package. Install it with "
        "`pip install requests` and try again."
    ) from exc


DEFAULT_OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:1.7b")


def _build_messages(prompt: str, system_prompt: Optional[str]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages


def _chat_request(
    *,
    url: str,
    model: str,
    prompt: str,
    system_prompt: Optional[str],
    stream: bool,
) -> Iterator[str] | str:
    payload = {
        "model": model,
        "messages": _build_messages(prompt, system_prompt),
        "stream": stream,
    }
    endpoint = f"{url.rstrip('/')}/api/chat"

    if stream:
        return _stream_chat(endpoint, payload)

    response = requests.post(endpoint, json=payload, timeout=300)
    response.raise_for_status()
    data = response.json()
    return data.get("message", {}).get("content", "")


def _stream_chat(endpoint: str, payload: dict[str, object]) -> Iterator[str]:
    response = requests.post(endpoint, json=payload, stream=True, timeout=300)
    response.raise_for_status()
    try:
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            packet = json.loads(line)
            if packet.get("done"):
                break
            chunk = packet.get("message", {}).get("content")
            if chunk:
                yield chunk
    finally:
        response.close()


def chat(
    prompt: str,
    *,
    url: str = DEFAULT_OLLAMA_URL,
    model: str = DEFAULT_MODEL,
    system_prompt: Optional[str] = None,
    stream: bool = False,
) -> Iterator[str] | str:
    """Send a prompt to the Ollama chat API and return the response."""

    try:
        return _chat_request(
            url=url,
            model=model,
            prompt=prompt,
            system_prompt=system_prompt,
            stream=stream,
        )
    except requests.exceptions.RequestException as exc:
        raise SystemExit(f"Ollama request failed: {exc}") from exc


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query a locally running Ollama Qwen3 1.7B model.",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="User prompt to send. If omitted, the prompt is read from stdin.",
    )
    parser.add_argument(
        "--system",
        dest="system_prompt",
        help="Optional system prompt to prepend before the user message.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Model name to use (default: %(default)s).",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_OLLAMA_URL,
        help="Base URL for the Ollama API (default: %(default)s).",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream tokens as they arrive instead of waiting for the full reply.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=1,
        help="Number of independent responses to generate (default: %(default)s).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write responses as JSON (saved automatically when top-k > 1).",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    prompt = args.prompt if args.prompt is not None else sys.stdin.read()

    if not prompt.strip():
        print("No prompt provided. Pass a prompt argument or pipe text via stdin.", file=sys.stderr)
        return 1

    if args.top_k < 1:
        print("--top-k must be at least 1.", file=sys.stderr)
        return 1

    if args.stream and args.top_k != 1:
        print("Streaming mode only supports --top-k=1.", file=sys.stderr)
        return 1

    if args.top_k == 1 and not args.output:
        result = chat(
            prompt,
            url=args.url,
            model=args.model,
            system_prompt=args.system_prompt,
            stream=args.stream,
        )

        if args.stream:
            assert not isinstance(result, str)  # narrow type for type checkers
            for chunk in result:
                print(chunk, end="", flush=True)
            print()
        else:
            assert isinstance(result, str)
            print(result)
        return 0

    responses = []
    for idx in range(args.top_k):
        result = chat(
            prompt,
            url=args.url,
            model=args.model,
            system_prompt=args.system_prompt,
            stream=False,
        )
        assert isinstance(result, str)
        responses.append({"index": idx, "content": result})

    record = {
        "model": args.model,
        "url": args.url,
        "prompt": prompt,
        "system_prompt": args.system_prompt,
        "count": args.top_k,
        "responses": responses,
    }

    output_path = args.output or Path("ollama_qwen_responses.json")
    output_path.write_text(json.dumps(record, indent=2))
    print(f"Saved {args.top_k} responses to {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
