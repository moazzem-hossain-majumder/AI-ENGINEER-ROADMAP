"""
Project 006: Token Budget & Cost Estimator
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates Byte Pair Encoding (BPE) sub-word tokenization,
calculates token metrics, and projects financial cost across leading models.
"""

import sys
from pathlib import Path
import tiktoken
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Ensure Windows terminals support UTF-8 characters and emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(force_terminal=True)


def analyze_tokens(text: str, encoding_name: str = "cl100k_base"):
    """Tokenizes text using tiktoken and visualizes sub-word boundaries."""
    encoding = tiktoken.get_encoding(encoding_name)
    token_ids = encoding.encode(text)
    
    # Decode each token individually to visualize sub-word chunks
    token_chunks = [encoding.decode([tid]) for tid in token_ids]

    console.print(Panel(f"[italic]{text}[/italic]", 
                        title="📝 [bold cyan]Input Text[/]", 
                        border_style="cyan"))

    # Render token boundary visualization with alternating colors
    rendered_tokens = Text()
    colors = ["bold bright_green", "bold bright_yellow", "bold bright_cyan", "bold bright_magenta"]
    for i, chunk in enumerate(token_chunks):
        color = colors[i % len(colors)]
        # Represent whitespace visibly if leading
        display_chunk = chunk.replace(" ", "·")
        rendered_tokens.append(f"[{display_chunk}]", style=color)

    console.print(Panel(rendered_tokens, 
                        title="🔍 [bold green]Sub-word Token Chunks (Colored Boundaries)[/]", 
                        border_style="green"))

    # Display Metrics Table
    num_chars = len(text)
    num_words = len(text.split())
    num_tokens = len(token_ids)
    char_to_token = num_chars / num_tokens if num_tokens > 0 else 0

    table = Table(title="📊 Tokenization Metrics", border_style="yellow")
    table.add_column("Metric", style="bold yellow")
    table.add_column("Value", style="cyan")

    table.add_row("Total Characters", str(num_chars))
    table.add_row("Total Words", str(num_words))
    table.add_row("Total Tokens", str(num_tokens))
    table.add_row("Avg Characters per Token", f"{char_to_token:.2f}")
    table.add_row("Encoding Standard", encoding_name)

    console.print(table)
    return num_tokens


def calculate_cost_projections(prompt_tokens: int, estimated_output_tokens: int = 250, num_requests: int = 50_000):
    """
    Calculates cost projections across popular industry models.
    Prices are per 1 Million tokens (standard pricing model).
    """
    models_pricing = [
        # (Model Name, Prompt Price / 1M tokens, Output Price / 1M tokens)
        ("Groq Cloud (qwen/qwen3.8-27b)", 0.09, 0.16),
        ("Google Gemini 1.5 Flash", 0.075, 0.30),
        ("OpenAI GPT-4o-mini", 0.15, 0.60),
        ("OpenAI GPT-4o", 2.50, 10.00),
        ("Anthropic Claude 3.5 Sonnet", 3.00, 15.00),
    ]

    total_prompt_tokens = prompt_tokens * num_requests
    total_output_tokens = estimated_output_tokens * num_requests

    cost_table = Table(
        title=f"💰 Cost Projection for {num_requests:,} API Requests\n"
              f"(Assuming {prompt_tokens} prompt tokens + {estimated_output_tokens} output tokens per request)",
        border_style="magenta"
    )
    cost_table.add_column("Model Provider", style="bold white", width=32)
    cost_table.add_column("Prompt Cost", style="green")
    cost_table.add_column("Output Cost", style="yellow")
    cost_table.add_column("Total Cost", style="bold cyan")

    for model, p_price, o_price in models_pricing:
        prompt_cost = (total_prompt_tokens / 1_000_000) * p_price
        output_cost = (total_output_tokens / 1_000_000) * o_price
        total_cost = prompt_cost + output_cost
        cost_table.add_row(
            model,
            f"${prompt_cost:,.2f}",
            f"${output_cost:,.2f}",
            f"${total_cost:,.2f}"
        )

    console.print(cost_table)


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 006: TOKEN BUDGET & COST   [/]")
    console.print("[bold yellow]===========================================================[/]\n")

    sample_text = (
        "Artificial intelligence engineering requires mastering RAG architectures, "
        "autonomous agent loops, and rigorous token budget management."
    )

    num_tokens = analyze_tokens(sample_text)
    calculate_cost_projections(prompt_tokens=num_tokens, estimated_output_tokens=250, num_requests=50_000)


if __name__ == "__main__":
    main()
