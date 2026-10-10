"""
Project 007: Few-Shot In-Context Learning
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates how Few-Shot demonstrations steer model classification,
enforcing an enterprise taxonomy without fine-tuning weights.
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

# Find and load root .env
root_dir = Path(__file__).resolve().parent.parent.parent
load_dotenv(root_dir / ".env")

console = Console(force_terminal=True)


def run_zero_shot(client: Groq, model: str, ticket: str) -> str:
    """Zero-shot: Prompt with no demonstration examples."""
    prompt = (
        "Classify the following customer ticket by category and urgency:\n\n"
        f"Ticket: {ticket}\n\n"
        "Classification:"
    )
    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=80
    )
    return res.choices[0].message.content.strip()


def run_few_shot(client: Groq, model: str, ticket: str) -> str:
    """Few-shot: Prompt equipped with canonical (Input -> Output) examples."""
    prompt = f"""You are an enterprise ticketing triage system.
Classify each customer ticket strictly using the following taxonomy:
Intent: [TECHNICAL_OUTAGE | BILLING_DISPUTE | FEATURE_REQUEST | ACCOUNT_ACCESS]
Sentiment: [HIGHLY_FRUSTRATED | NEUTRAL | SATISFIED]
Priority: [P1_CRITICAL | P2_HIGH | P3_NORMAL]
Action: [Page On-Call | Escalate to Billing | Queue for Product | Send Password Reset]

---
Example 1:
Ticket: "I was charged twice on my credit card for invoice #INV-9201. Please reverse the duplicate charge."
Intent: BILLING_DISPUTE
Sentiment: NEUTRAL
Priority: P2_HIGH
Action: Escalate to Billing

---
Example 2:
Ticket: "Would love to see dark mode added to the analytics dashboard in the next quarterly release!"
Intent: FEATURE_REQUEST
Sentiment: SATISFIED
Priority: P3_NORMAL
Action: Queue for Product

---
Example 3:
Ticket: "Our entire production API is returning 502 Bad Gateway! Customers can't checkout!"
Intent: TECHNICAL_OUTAGE
Sentiment: HIGHLY_FRUSTRATED
Priority: P1_CRITICAL
Action: Page On-Call

---
Ticket: "{ticket}"
"""
    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=80
    )
    return res.choices[0].message.content.strip()


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 007: FEW-SHOT PROMPTING    [/]")
    console.print("[bold yellow]===========================================================[/]\n")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    model = "qwen/qwen3.8-27b"

    # Ambiguous, high-stakes customer ticket
    test_ticket = (
        "We lost all access to our production database immediately after renewing our "
        "annual enterprise billing contract this morning! Fix this immediately, our business is halted!"
    )

    console.print(Panel(f"[bold white]{test_ticket}[/]", 
                        title="🎫 [bold yellow]Incoming Customer Support Ticket[/]", 
                        border_style="yellow"))

    # 1. Execute Zero-Shot
    zero_shot_res = run_zero_shot(client, model, test_ticket)
    console.print(Panel(zero_shot_res, 
                        title="❌ [bold red]Zero-Shot Output (Unpredictable Structure & Labels)[/]", 
                        border_style="red"))

    # 2. Execute Few-Shot
    few_shot_res = run_few_shot(client, model, test_ticket)
    console.print(Panel(few_shot_res, 
                        title="✅ [bold green]Few-Shot Output (Strict Enterprise Taxonomy)[/]", 
                        border_style="green"))

    # Parse few-shot response lines into structured table
    table = Table(title="✨ Parsed Few-Shot Classification Results", border_style="cyan")
    table.add_column("Taxonomy Key", style="bold yellow", width=18)
    table.add_column("Assigned Value", style="white")

    for line in few_shot_res.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            table.add_row(key.strip(), val.strip())

    if table.rows:
        console.print(table)


if __name__ == "__main__":
    main()
