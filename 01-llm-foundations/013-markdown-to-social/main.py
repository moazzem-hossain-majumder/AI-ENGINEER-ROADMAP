"""
Project 013: Markdown-to-Social Content Transformer
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates multi-format technical content transformation: transforming
engineering markdown into audited X/Twitter threads, LinkedIn articles,
and newsletter summaries using Pydantic V2 schemas.
"""

import os
import sys
import json
from typing import List
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
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


class SocialBundle(BaseModel):
    x_thread: List[str] = Field(description="List of 3 numbered tweets. Each tweet must be strictly under 260 characters.")
    linkedin_post: str = Field(description="Formatted LinkedIn article with hook, bullets, and closing question.")
    newsletter_tldr: str = Field(description="50-word concise newsletter summary with bulleted takeaways.")


def transform_technical_content(markdown_text: str) -> SocialBundle:
    """Uses LLM to repurpose technical markdown into a multi-platform social bundle."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env")

    client = Groq(api_key=api_key)
    model = "qwen/qwen3.8-27b"

    schema_str = json.dumps(SocialBundle.model_json_schema(), indent=2)

    system_prompt = (
        "You are an expert technical developer advocate and content strategist. "
        "Transform the provided engineering blog post into high-impact social media assets.\n\n"
        "STRICT PLATFORM RULES:\n"
        "1. X/Twitter Thread: Exactly 3 tweets. Each tweet MUST be under 260 characters. Number them (1/3), (2/3), (3/3).\n"
        "2. LinkedIn: Professional tone, clear line breaks for mobile reading, 2-3 value bullet points, and an engagement question.\n"
        "3. Newsletter: Under 60 words total.\n\n"
        f"Output strictly valid JSON matching this schema:\n{schema_str}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Source Markdown Document:\n\n{markdown_text}"}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )

    raw_json = response.choices[0].message.content
    return SocialBundle.model_validate_json(raw_json)


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 013: CONTENT TRANSFORMER   [/]")
    console.print("[bold yellow]===========================================================[/]\n")

    markdown_doc = """
# Scaling Vector Search: How We Scaled RAG from 10k to 10M Documents

When our engineering team initially deployed our Retrieval-Augmented Generation (RAG) system, we used a naive flat vector index. It worked seamlessly at 10,000 documents with sub-10ms query latency.

However, as our corpus scaled to 10,000,000 documents, performance collapsed:
1. Memory Consumption: In-memory uncompressed 1536-dimensional float32 vectors required 60+ GB of expensive GPU VRAM.
2. Search Latency: Flat L2 distance scans spiked from 8ms to 420ms, violating our production SLA.

To resolve this bottleneck, we engineered three architectural upgrades:
- HNSW Graph Indexing with Scalar Quantization (SQ8): Compressed vector footprints by 75% while maintaining 98.4% recall.
- Parent-Document Multi-Vector Retrieval: We decoupled chunk indexing from prompt context. We search across small 200-token chunks for precision, but return the 1,500-token parent document to the LLM for grounded context.
- Hybrid Search with Reciprocal Rank Fusion (RRF): Blended BM25 keyword matching with dense vectors, eliminating acronym hallucination.

Result: P99 latency dropped back down to 14ms across 10 million documents.
"""

    console.print(Panel(markdown_doc[:450] + "...\n[dim](truncated for display)[/dim]", 
                        title="📄 [bold cyan]Source Technical Markdown Document[/]", 
                        border_style="cyan"))

    console.print("[bold yellow]⚙️ Transforming content into multi-platform social bundle...[/]\n")
    bundle = transform_technical_content(markdown_doc)

    # 1. Display X / Twitter Thread with character length audits
    console.print("[bold bright_cyan]🐦 Platform 1: X (Twitter) Thread (Audit: Max 280 chars per tweet)[/]")
    for i, tweet in enumerate(bundle.x_thread, 1):
        char_len = len(tweet)
        status = "[green]✅ Valid[/green]" if char_len <= 280 else "[red]❌ Over limit[/red]"
        console.print(Panel(
            tweet,
            title=f"Tweet {i}/{len(bundle.x_thread)} (Length: {char_len} chars | {status})",
            border_style="bright_cyan"
        ))

    # 2. Display LinkedIn Article
    console.print("\n[bold bright_green]💼 Platform 2: LinkedIn Technical Article[/]")
    console.print(Panel(
        bundle.linkedin_post,
        title="LinkedIn Feed Post",
        border_style="bright_green"
    ))

    # 3. Display Newsletter TL;DR
    console.print("\n[bold bright_magenta]📬 Platform 3: Email Newsletter TL;DR[/]")
    console.print(Panel(
        bundle.newsletter_tldr,
        title="Substack / Newsletter Summary",
        border_style="bright_magenta"
    ))


if __name__ == "__main__":
    main()
