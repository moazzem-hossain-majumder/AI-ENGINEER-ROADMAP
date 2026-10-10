"""
Project 014: Error Handling, Exponential Backoff & Provider Fallback
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates production reliability engineering: handling rate limits,
applying exponential backoff with jitter, and automatic failover from
primary provider (Groq) to secondary provider (Google Gemini).
"""

import os
import sys
import time
import random
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq, RateLimitError, APIConnectionError, APIStatusError
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


def calculate_jittered_backoff(attempt: int, base: float = 0.5, max_sleep: float = 4.0) -> float:
    """Calculates truncated exponential backoff with full jitter."""
    calculated_ceiling = min(max_sleep, base * (2 ** attempt))
    delay = random.uniform(base, calculated_ceiling)
    return delay


def call_primary_groq(prompt: str, simulate_outage: bool = False) -> str:
    """Attempts generation via Groq Cloud with retry and backoff."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY missing.")

    client = Groq(api_key=api_key)
    # If simulating an outage, intentionally use an invalid model that forces an API error
    model_name = "invalid-outage-model" if simulate_outage else "qwen/qwen3.8-27b"

    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            if simulate_outage and attempt == 0:
                console.print("[dim yellow]  ↳ [Primary: Groq] Attempting request (outage simulated)...[/dim yellow]")
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=80
            )
            return response.choices[0].message.content.strip()
        except (RateLimitError, APIConnectionError, APIStatusError, Exception) as err:
            if attempt < max_retries:
                delay = calculate_jittered_backoff(attempt)
                console.print(f"[bold yellow]  ⚠️ [Primary Glitch]:[/] {type(err).__name__}. "
                              f"Applying backoff: sleeping {delay:.2f}s (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(delay)
            else:
                console.print(f"[bold red]  ❌ [Primary Exhausted]:[/] Retries failed. Initiating circuit failover.")
                raise err


def call_secondary_gemini(prompt: str) -> str:
    """Fallback handler: routes request to Google Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY missing.")

    from google import genai
    client = genai.Client(api_key=api_key)

    console.print("[bold cyan]  🔄 [Fallback Router]:[/] Routing to Secondary Provider: [magenta]Google Gemini[/]...")
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt
    )
    return response.text.strip()


def execute_resilient_prompt(prompt: str, simulate_primary_failure: bool = False) -> tuple[str, str, float]:
    """Orchestrates primary execution with automatic secondary failover."""
    start_time = time.perf_counter()
    provider_used = "Groq Cloud"

    try:
        result = call_primary_groq(prompt, simulate_outage=simulate_primary_failure)
    except Exception:
        # Primary failed completely, invoke secondary fallback!
        provider_used = "Google Gemini (Fallback)"
        result = call_secondary_gemini(prompt)

    duration = time.perf_counter() - start_time
    return result, provider_used, duration


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 014: RESILIENT RETRY & FALLBACK[/]")
    console.print("[bold yellow]===========================================================[/]\n")

    test_prompt = "Explain in one sentence why exponential backoff prevents API retry storms."

    # Scenario 1: Normal Primary Execution
    console.print("[bold cyan]Scenario 1: Normal Primary Execution (Groq Cloud)[/]")
    result, provider, duration = execute_resilient_prompt(test_prompt, simulate_primary_failure=False)
    console.print(Panel(
        f"[bold white]{result}[/]\n\n[dim]Provider: {provider} | Latency: {duration:.2f}s | Status: 200 OK[/dim]",
        title="🚀 [bold green]Primary Provider Succeeded[/]",
        border_style="green"
    ))

    # Scenario 2: Simulated Primary Outage with Automatic Failover to Gemini
    console.print("\n[bold yellow]Scenario 2: Primary Outage Simulation ➔ Automatic Failover to Gemini[/]")
    result_fallback, provider_fallback, duration_fallback = execute_resilient_prompt(test_prompt, simulate_primary_failure=True)
    console.print(Panel(
        f"[bold white]{result_fallback}[/]\n\n[dim]Provider: {provider_fallback} | Latency: {duration_fallback:.2f}s | Status: Recovered via Fallback[/dim]",
        title="🌟 [bold magenta]Secondary Provider Fallback Succeeded[/]",
        border_style="magenta"
    ))

    console.print("\n[bold green]✔ Resilience Verification Complete:[/] System maintained 100% uptime through multi-provider routing!")


if __name__ == "__main__":
    main()
