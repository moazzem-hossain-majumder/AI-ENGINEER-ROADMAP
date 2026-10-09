"""
Project 005: Streaming & Real-Time Token Delivery
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates real-time token streaming with stream=True, measures
Time-to-First-Token (TTFT), and calculates generation throughput (Tokens/sec).
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.table import Table

# Ensure Windows terminals support UTF-8 characters and emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Find and load root .env
root_dir = Path(__file__).resolve().parent.parent.parent
load_dotenv(root_dir / ".env")

console = Console(force_terminal=True)


def stream_llm_response(prompt: str, model: str = "qwen/qwen3.8-27b"):
    """Streams LLM tokens live while measuring performance telemetry."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)

    console.print(f"[bold cyan]Prompt:[/] [italic]{prompt}[/italic]\n")
    console.print("[bold green]Streaming output live...[/]\n")

    # Start timing
    start_time = time.perf_counter()
    first_token_time = None
    chunks_received = 0
    full_text = []

    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an insightful AI educator. Provide a structured 3-point explanation."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300,
        stream=True  # Enables Server-Sent Events (SSE) streaming!
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        content_piece = delta.content or ""
        
        if content_piece:
            if first_token_time is None:
                first_token_time = time.perf_counter()
            
            chunks_received += 1
            full_text.append(content_piece)
            
            # Print token immediately as it arrives across the network
            sys.stdout.write(content_piece)
            sys.stdout.flush()

    end_time = time.perf_counter()
    sys.stdout.write("\n\n")

    # Compute latency & throughput metrics
    total_duration = end_time - start_time
    ttft = (first_token_time - start_time) if first_token_time else 0.0
    generation_duration = (end_time - first_token_time) if first_token_time else 0.0
    tokens_per_sec = (chunks_received / generation_duration) if generation_duration > 0 else 0.0

    # Display telemetry
    table = Table(title="⚡ Streaming Performance Telemetry", border_style="magenta")
    table.add_column("Metric", style="bold yellow", width=30)
    table.add_column("Measurement", style="cyan")

    table.add_row("Model", model)
    table.add_row("Time-to-First-Token (TTFT)", f"{ttft * 1000:.1f} ms")
    table.add_row("Total Generation Time", f"{total_duration:.2f} s")
    table.add_row("Chunks / Tokens Streamed", str(chunks_received))
    table.add_row("Generation Speed", f"{tokens_per_sec:.1f} tokens/sec")

    console.print(table)


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 005: TOKEN STREAMING       [/]")
    console.print("[bold yellow]===========================================================[/]\n")

    test_prompt = "Why is streaming critical when building production AI web applications?"
    stream_llm_response(test_prompt)


if __name__ == "__main__":
    main()
