#!/usr/bin/env python3
"""Minimal client for talking to a local Ollama Qwen3 1.7B model.

The script sends chat-style prompts to the Ollama REST API.  By default it
targets a local daemon (`http://localhost:11434`) and the `qwen3:1.7b` model,
but both can be overridden with CLI flags or environment variables.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Iterator, Optional

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
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    prompt = args.prompt if args.prompt is not None else sys.stdin.read()

    if not prompt.strip():
        print("No prompt provided. Pass a prompt argument or pipe text via stdin.", file=sys.stderr)
        return 1

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


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
