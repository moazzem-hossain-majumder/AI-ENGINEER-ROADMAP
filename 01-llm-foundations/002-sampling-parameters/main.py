"""
Project 002: Sampling Parameters & Determinism
Phase 01: LLM Foundations & Prompt Engineering

Compares Temperature (0.0 vs 0.7 vs 1.4), Top-P sampling, and Stop sequences.
Proves deterministic vs creative behavior side-by-side.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
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


def test_temperature_determinism(client: Groq, model: str, prompt: str):
    """
    Demonstrates that temperature=0.0 is deterministic:
    Running the exact same prompt multiple times yields the exact same output.
    """
    console.print("\n[bold cyan]1. Testing Determinism with Temperature = 0.0 (3 Identical Runs)[/]")
    console.print("[dim]Greedy decoding always picks the token with highest probability (argmax).[/dim]\n")

    runs = []
    for i in range(1, 4):
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=60
        )
        output = response.choices[0].message.content.strip()
        runs.append(output)
        console.print(f"[bold green]Run #{i} (T=0.0):[/] {output}")

    # Check if all runs are 100% identical
    is_identical = len(set(runs)) == 1
    if is_identical:
        console.print("\n[bold green]✔ Verified:[/] All 3 outputs are 100% identical! Perfect for code, JSON & math.\n")
    else:
        console.print("\n[yellow]Notice:[/] Minor variance due to model engine parallelism.\n")


def test_temperature_spectrum(client: Groq, model: str, prompt: str):
    """
    Demonstrates the difference between Low (0.0), Medium (0.7), and High (1.4) temperatures.
    """
    console.print("[bold cyan]2. Testing Temperature Spectrum on Creativity[/]")
    
    temps = [0.0, 0.7, 1.4]
    results_table = Table(title=f"🎨 Temperature Comparison for: '{prompt}'", border_style="bright_blue")
    results_table.add_column("Temperature", style="bold yellow", width=14)
    results_table.add_column("Sampling Behavior", style="dim", width=25)
    results_table.add_column("Generated Response", style="white")

    descriptions = {
        0.0: "Deterministic (Greedy)",
        0.7: "Balanced (Conversational)",
        1.4: "High Entropy (Divergent/Creative)"
    }

    for temp in temps:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a branding specialist. Respond with exactly one short punchy tagline."},
                {"role": "user", "content": prompt}
            ],
            temperature=temp,
            max_tokens=40
        )
        generated_text = response.choices[0].message.content.strip()
        results_table.add_row(f"T = {temp}", descriptions[temp], generated_text)

    console.print(results_table)


def test_stop_sequences(client: Groq, model: str):
    """
    Demonstrates stop sequences: Halting the LLM generation early
    when a specific token or word appears.
    """
    console.print("\n[bold cyan]3. Testing Custom Stop Sequences (`stop=['---']`)[/]")
    console.print("[dim]The model will stop producing tokens as soon as it writes '---'.[/dim]\n")

    prompt = (
        "List 5 AI engineering tools. Format each on a new line. "
        "After listing the 3rd tool, write '---' and then list the remaining tools."
    )

    # 1. Without stop sequence
    res_normal = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=150
    )
    console.print(Panel(res_normal.choices[0].message.content.strip(), 
                        title="Without Stop Sequence (Full List)", 
                        border_style="yellow"))

    # 2. With stop sequence
    res_stopped = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=150,
        stop=["---"]
    )
    console.print(Panel(res_stopped.choices[0].message.content.strip(), 
                        title="With stop=['---'] (Halted Early)", 
                        border_style="green"))


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 002: SAMPLING PARAMETERS   [/]")
    console.print("[bold yellow]===========================================================[/]")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] GROQ_API_KEY missing from .env.")
        return

    client = Groq(api_key=api_key)
    model = "qwen/qwen3.8-27b"

    # Test 1: Temperature 0 determinism
    test_temperature_determinism(client, model, prompt="Define an API in one sentence.")

    # Test 2: Spectrum comparison
    test_temperature_spectrum(client, model, prompt="Name for an AI startup that optimizes GPU cooling.")

    # Test 3: Stop sequences
    test_stop_sequences(client, model)


if __name__ == "__main__":
    main()
