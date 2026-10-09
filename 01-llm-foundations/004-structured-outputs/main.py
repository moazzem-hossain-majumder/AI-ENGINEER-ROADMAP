"""
Project 004: Structured Outputs & Schema Validation
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates extracting unstructured natural text into strongly typed,
schema-validated JSON objects using Pydantic V2 and LLM JSON Mode.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
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


# 1. Define Pydantic Schema (The Data Contract)
class JobPosting(BaseModel):
    title: str = Field(description="Official job title")
    company: str = Field(description="Company or organization hiring")
    locations: List[str] = Field(description="List of physical or remote locations")
    is_remote_friendly: bool = Field(description="True if remote work is permitted")
    min_years_experience: int = Field(description="Minimum years of required experience")
    required_skills: List[str] = Field(description="Technical skills explicitly requested")
    min_salary_usd: Optional[int] = Field(None, description="Lower bound of salary in USD")
    max_salary_usd: Optional[int] = Field(None, description="Upper bound of salary in USD")


def extract_job_posting(unstructured_text: str) -> Optional[JobPosting]:
    """Uses LLM in JSON mode to extract strongly typed JobPosting data."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] GROQ_API_KEY not found in .env")
        return None

    client = Groq(api_key=api_key)

    # Export Pydantic schema as JSON schema for system prompt injection
    schema_str = json.dumps(JobPosting.model_json_schema(), indent=2)

    system_prompt = (
        "You are an expert data extraction assistant. "
        "Extract the information from the user's text and output ONLY valid JSON "
        "adhering strictly to the following JSON schema:\n\n"
        f"{schema_str}\n\n"
        "Do NOT include markdown backticks or commentary. Output raw JSON only."
    )

    console.print(Panel(f"[dim]{unstructured_text}[/dim]", 
                        title="📄 [bold yellow]Raw Unstructured Job Description Input[/]", 
                        border_style="yellow"))

    # Execute completion in JSON mode
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": unstructured_text}
        ],
        temperature=0.0,  # Zero temperature for deterministic extraction
        response_format={"type": "json_object"}
    )

    raw_json = response.choices[0].message.content
    console.print(Panel(f"[bold cyan]{raw_json}[/]", 
                        title="🔍 [bold cyan]Raw JSON Returned by LLM (JSON Mode)[/]", 
                        border_style="cyan"))

    # Validate with Pydantic
    try:
        job = JobPosting.model_validate_json(raw_json)
        return job
    except ValidationError as err:
        console.print(f"[bold red]Validation Error:[/] {err}")
        return None


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 004: STRUCTURED OUTPUTS    [/]")
    console.print("[bold yellow]===========================================================[/]\n")

    messy_text = (
        "Synthetix AI is searching for a Lead Machine Learning Engineer! "
        "Our headquarters are based in San Francisco, CA, but this role can be 100% remote anywhere in the US. "
        "Applicants should have at least 5 years of production coding experience with Python. "
        "Key qualifications include deep expertise with PyTorch, Vector Databases like Chroma or Pinecone, "
        "and experience deploying RAG pipelines. We offer a competitive base compensation of "
        "$190,000 to $240,000 plus substantial equity and full medical benefits."
    )

    job = extract_job_posting(messy_text)

    if job:
        table = Table(title="✨ Validated Pydantic JobPosting Object", border_style="green")
        table.add_column("Field", style="bold yellow", width=22)
        table.add_column("Validated Value", style="white")

        table.add_row("Title", job.title)
        table.add_row("Company", job.company)
        table.add_row("Locations", ", ".join(job.locations))
        table.add_row("Remote Friendly", "✅ Yes" if job.is_remote_friendly else "❌ No")
        table.add_row("Min Experience", f"{job.min_years_experience} years")
        table.add_row("Required Skills", ", ".join(job.required_skills))
        table.add_row("Salary Range (USD)", f"${job.min_salary_usd:,.0f} - ${job.max_salary_usd:,.0f}" if job.min_salary_usd else "Not specified")

        console.print(table)
        console.print("\n[bold green]✔ Success:[/] Object is now a strongly typed Python instance ready for database storage!")


if __name__ == "__main__":
    main()
