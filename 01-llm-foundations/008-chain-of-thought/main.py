"""
Project 008: Chain-of-Thought (CoT) Reasoning
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates how Chain-of-Thought reasoning improves multi-step logic
and arithmetic, using structured XML scratchpads (<thinking> and <answer>).
"""

import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.panel import Panel

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


def solve_with_direct_answer(client: Groq, model: str, problem: str) -> str:
    """Prompts model for an immediate, direct answer without scratchpad."""
    prompt = (
        "Answer the following problem directly. Do NOT explain your work, "
        "just state the final number and unit:\n\n"
        f"Problem: {problem}"
    )
    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=50
    )
    return res.choices[0].message.content.strip()


def solve_with_chain_of_thought(client: Groq, model: str, problem: str) -> tuple[str, str]:
    """Prompts model with structured CoT scratchpad (<thinking> and <answer> tags)."""
    system_prompt = (
        "You are an expert mathematical and logical reasoning engine. "
        "You must solve complex problems by breaking them down into sequential steps.\n\n"
        "Format your response strictly using this structure:\n"
        "<thinking>\n"
        "[List every single deduction and arithmetic step explicitly]\n"
        "</thinking>\n"
        "<answer>\n"
        "[The concise final verified answer with units]\n"
        "</answer>"
    )

    user_prompt = f"Problem: {problem}"

    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        max_tokens=350
    )

    full_output = res.choices[0].message.content.strip()

    # Parse XML tags using regex
    thinking_match = re.search(r"<thinking>(.*?)</thinking>", full_output, re.DOTALL)
    answer_match = re.search(r"<answer>(.*?)</answer>", full_output, re.DOTALL)

    thinking = thinking_match.group(1).strip() if thinking_match else "Reasoning trace not found."
    answer = answer_match.group(1).strip() if answer_match else full_output

    return thinking, answer


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 008: CHAIN-OF-THOUGHT      [/]")
    console.print("[bold yellow]===========================================================[/]\n")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    model = "qwen/qwen3.8-27b"

    # Multi-step distributed infrastructure arithmetic puzzle
    problem = (
        "A cloud server cluster has 12 nodes. Each node hosts 8 virtual machines. "
        "During morning peak, 25% of all VMs process database tasks. Half of the remaining "
        "VMs run AI inference jobs. Each AI inference job requires 3 GPU cores. "
        "How many GPU cores are needed in total?"
    )

    console.print(Panel(f"[bold white]{problem}[/]", 
                        title="🧩 [bold cyan]Multi-Step Infrastructure Logic Puzzle[/]", 
                        border_style="cyan"))

    # 1. Direct answer attempt
    direct_ans = solve_with_direct_answer(client, model, problem)
    console.print(Panel(f"[bold yellow]{direct_ans}[/]", 
                        title="⚡ [bold yellow]Direct Answer (No Scratchpad)[/]", 
                        border_style="yellow"))

    # 2. Structured CoT
    thinking, answer = solve_with_chain_of_thought(client, model, problem)
    
    console.print(Panel(f"[dim]{thinking}[/dim]", 
                        title="🧠 [bold magenta]Chain-of-Thought Scratchpad (<thinking>)[/]", 
                        border_style="magenta"))

    console.print(Panel(f"[bold green]{answer}[/]", 
                        title="🎯 [bold green]Verified Final Solution (<answer>)[/]", 
                        border_style="green"))


if __name__ == "__main__":
    main()
