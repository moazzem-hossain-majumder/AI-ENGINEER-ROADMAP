"""
Project 011: Dynamic System Personas & Tone Control
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates how system prompts condition vocabulary, tone, and audience
adaptation by explaining the same technical topic across 3 distinct personas.
"""

import os
import sys
from dataclasses import dataclass
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


@dataclass
class Persona:
    name: str
    emoji: str
    title: str
    border_style: str
    system_prompt: str


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 011: ROLE-PLAYING PERSONA  [/]")
    console.print("[bold yellow]===========================================================[/]\n")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    model = "qwen/qwen3.8-27b"

    # Define 3 starkly different personas
    personas = [
        Persona(
            name="ELI5",
            emoji="🧸",
            title="Explain Like I'm 5 (Kindergarten Teacher)",
            border_style="bright_cyan",
            system_prompt=(
                "You are a warm, imaginative kindergarten teacher speaking to a 5-year-old. "
                "Explain everything using simple toy or candy metaphors. "
                "STRICT RULES: Use ZERO technical jargon. No math words. Keep it under 3 friendly sentences."
            )
        ),
        Persona(
            name="Principal Systems Engineer",
            emoji="💻",
            title="Principal Distributed Systems & AI Infrastructure Architect",
            border_style="bright_green",
            system_prompt=(
                "You are a world-class Principal AI Infrastructure Architect speaking to senior engineers. "
                "Explain the concept with maximum mathematical and architectural rigor. "
                "Use terms like high-dimensional vectors, cosine distance, HNSW graphs, and latency. "
                "Keep your response strictly under 3 dense, authoritative sentences."
            )
        ),
        Persona(
            name="Enterprise Legal Counsel",
            emoji="⚖️",
            title="Corporate General Counsel & AI Compliance Officer",
            border_style="bright_yellow",
            system_prompt=(
                "You are an enterprise corporate general counsel and data compliance officer. "
                "Explain the concept strictly through the lens of intellectual property risk, "
                "PII data governance, copyright liability, and enterprise contractual compliance. "
                "Keep your response strictly under 3 formal legal sentences."
            )
        ),
    ]

    topic = "What is a Vector Embedding and why do we use it in AI?"
    console.print(Panel(f"[bold white]{topic}[/]", 
                        title="📌 [bold cyan]Core Technical Topic to Explain[/]", 
                        border_style="cyan"))

    for p in personas:
        console.print(f"\n[dim]Generating response for persona: {p.name}...[/]")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": p.system_prompt},
                {"role": "user", "content": topic}
            ],
            temperature=0.7,
            max_tokens=180
        )
        content = response.choices[0].message.content.strip()

        console.print(Panel(
            f"[bold white]{content}[/]",
            title=f"{p.emoji} [bold {p.border_style}]Persona: {p.title}[/]",
            border_style=p.border_style
        ))


if __name__ == "__main__":
    main()
