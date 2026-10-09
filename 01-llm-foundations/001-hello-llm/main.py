"""
Project 001: Hello LLM (Anatomy of an LLM API Call)
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates the fundamental mechanics of sending a prompt to an LLM
and extracting both the generated content and execution metadata.
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Ensure Windows terminals support UTF-8 characters and emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Find and load the root .env file
root_dir = Path(__file__).resolve().parent.parent.parent
load_dotenv(root_dir / ".env")

console = Console(force_terminal=True)


def run_groq_example():
    """Execute API call via Groq Cloud (Ultra-fast inference)."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] GROQ_API_KEY not found in .env file.")
        return

    try:
        from groq import Groq
    except ImportError:
        console.print("[bold red]Error:[/] groq package not installed. Run: pip install groq")
        return

    client = Groq(api_key=api_key)
    
    # High-performance chat model on Groq
    model_name = "qwen/qwen3.8-27b"
    
    system_prompt = (
        "You are an encouraging, world-class AI engineering mentor. "
        "Keep your response strictly under 2 sentences."
    )
    user_prompt = "What is the single most important skill for an AI Engineer in 2026?"

    console.print(Panel(f"[bold cyan]Provider:[/] Groq Cloud\n"
                        f"[bold cyan]Model:[/] {model_name}\n"
                        f"[bold yellow]System Prompt:[/] {system_prompt}\n"
                        f"[bold green]User Prompt:[/] {user_prompt}",
                        title="🚀 [bold blue]Project 001: Outgoing API Request[/]"))

    start_time = time.time()
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )
    elapsed = time.time() - start_time

    # 1. Extract generated answer
    answer = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason

    # 2. Extract token usage metadata
    usage = response.usage
    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    total_tokens = usage.total_tokens

    # Display Answer
    console.print(Panel(f"[bold white]{answer}[/]", 
                        title="🤖 [bold green]Model Response[/]", 
                        border_style="green"))

    # Display Metadata Table
    table = Table(title="📊 Request Execution Metadata", border_style="cyan")
    table.add_column("Metric", style="bold yellow")
    table.add_column("Value", style="cyan")

    table.add_row("Model Used", model_name)
    table.add_row("Finish Reason", str(finish_reason))
    table.add_row("Prompt Tokens (Input)", str(prompt_tokens))
    table.add_row("Completion Tokens (Output)", str(completion_tokens))
    table.add_row("Total Tokens", str(total_tokens))
    table.add_row("Latency", f"{elapsed:.2f} seconds")

    console.print(table)


def run_gemini_example():
    """Execute API call via Google Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        console.print("\n[bold magenta]Testing Google Gemini Provider...[/]")
        start_time = time.time()
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents='Explain what an LLM token is in one short sentence.'
        )
        elapsed = time.time() - start_time
        
        console.print(Panel(f"[bold white]{response.text}[/]\n\n"
                            f"[dim]Latency: {elapsed:.2f}s | Model: gemini-3.8-flash[/dim]",
                            title="🌟 [bold magenta]Google Gemini Response[/]",
                            border_style="magenta"))
    except Exception as e:
        console.print(f"[yellow]Gemini note: {e}[/]")


if __name__ == "__main__":
    console.print("[bold yellow]====================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 001: HELLO LLM     [/]")
    console.print("[bold yellow]====================================================\n[/]")
    
    # 1. Run Groq API call
    run_groq_example()
    
    # 2. Run Gemini API call
    run_gemini_example()
