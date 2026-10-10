"""
Project 009: Prompt Templates & Dynamic Interpolation
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates production prompt template engineering: variable parsing,
strict schema validation, partial parameter binding, and safe LLM dispatch.
"""

import os
import re
import sys
from typing import Dict, List, Set, Any
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


class PromptTemplate:
    """Production prompt template with parameter extraction and strict validation."""

    def __init__(self, template: str, system_prompt: str = "You are a helpful assistant."):
        self.template = template
        self.system_prompt = system_prompt
        # Identify all {variable_name} placeholders using regex
        self.expected_vars: Set[str] = set(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", template))

    def format(self, **kwargs: Any) -> str:
        """Validates all required parameters are present, then formats the string."""
        provided_vars = set(kwargs.keys())
        missing_vars = self.expected_vars - provided_vars

        if missing_vars:
            raise ValueError(
                f"Missing required template variables: {sorted(list(missing_vars))}. "
                f"Provided: {sorted(list(provided_vars))}"
            )

        return self.template.format(**kwargs)

    def format_messages(self, **kwargs: Any) -> List[Dict[str, str]]:
        """Returns standard OpenAI/Groq message objects array."""
        user_content = self.format(**kwargs)
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content}
        ]

    def partial(self, **fixed_kwargs: Any) -> "PromptTemplate":
        """Returns a new PromptTemplate with a subset of parameters pre-filled."""
        # Replace only the provided keys in the template
        new_template = self.template
        for key, value in fixed_kwargs.items():
            new_template = new_template.replace(f"{{{key}}}", str(value))
        return PromptTemplate(template=new_template, system_prompt=self.system_prompt)


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 009: PROMPT TEMPLATES      [/]")
    console.print("[bold yellow]===========================================================[/]\n")

    # 1. Define the parameterized master template
    outreach_template_text = (
        "Write a compelling, concise enterprise partnership email to {prospect_name}, who is "
        "leading infrastructure at {prospect_company}.\n\n"
        "Reference their recent milestone: '{recent_milestone}'.\n"
        "Address their core pain point: '{pain_point}'.\n"
        "Position our solution: '{solution_value}'.\n"
        "Call to action: Ask for a short 10-minute briefing next week.\n"
        "Keep the tone direct, technical, and respectful of an executive's time."
    )

    template = PromptTemplate(
        template=outreach_template_text,
        system_prompt="You are a seasoned Silicon Valley enterprise partnership director. Avoid corporate fluff."
    )

    # 2. Inspect variables
    table = Table(title="📋 Template Variable Contract", border_style="cyan")
    table.add_column("Placeholder Variable", style="bold yellow")
    table.add_column("Status", style="green")

    for var in sorted(template.expected_vars):
        table.add_row(f"{{{var}}}", "Required")
    console.print(table)

    # 3. Defensive Validation Test (simulate missing param)
    console.print("\n[bold cyan]🛡️ Running Defensive Validation Test (Missing Parameter)...[/]")
    try:
        # Intentionally omit 'recent_milestone'
        template.format(
            prospect_name="Satya",
            prospect_company="Microsoft",
            pain_point="High GPU memory footprint",
            solution_value="Dynamic KV-cache compression"
        )
    except ValueError as e:
        console.print(Panel(f"[bold red]Caught Expected Error:[/] {e}", 
                            title="✔ Validation Guardrail Active", 
                            border_style="red"))

    # 4. Correctly populate and send to LLM
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    model = "qwen/qwen3.8-27b"

    params = {
        "prospect_name": "Satya",
        "prospect_company": "Microsoft",
        "recent_milestone": "Expansion of Azure hyperscale data centers",
        "pain_point": "Inference memory bottlenecks and rising power consumption",
        "solution_value": "Synthetix AI's dynamic KV-cache compression engine (40% RAM savings)",
    }

    messages = template.format_messages(**params)

    console.print(Panel(f"[dim]{messages[1]['content']}[/dim]", 
                        title="🚀 [bold yellow]Rendered User Prompt Dispatched to LLM[/]", 
                        border_style="yellow"))

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=300
    )

    generated_email = response.choices[0].message.content.strip()

    console.print(Panel(f"[bold white]{generated_email}[/]", 
                        title="📧 [bold green]Generated Personalized Executive Email[/]", 
                        border_style="green"))


if __name__ == "__main__":
    main()
