"""
Project 012: Map-Reduce Chunked Text Summarizer
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates the two-stage Map-Reduce summarization architecture for large
documents: local chunk extraction (Map) followed by global synthesis (Reduce).
"""

import os
import sys
from typing import List
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


def chunk_document(text: str, max_chunk_chars: int = 800) -> List[str]:
    """Splits text into paragraph-preserving semantic chunks."""
    paragraphs = text.strip().split("\n\n")
    chunks = []
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if current_length + len(para) > max_chunk_chars and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_length = len(para)
        else:
            current_chunk.append(para)
            current_length += len(para)

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
    return chunks


def map_summarize(client: Groq, model: str, chunk: str, chunk_idx: int, total_chunks: int) -> str:
    """Map Step: Summarizes an individual chunk to extract localized facts."""
    system_prompt = (
        "You are an expert technical intelligence analyst. "
        "Extract the 2 most critical factual takeaways, metrics, or decisions from this section. "
        "Format strictly as concise bullet points. Be completely factual."
    )
    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Section text:\n{chunk}"}
        ],
        temperature=0.0,
        max_tokens=150
    )
    return res.choices[0].message.content.strip()


def reduce_synthesize(client: Groq, model: str, intermediate_summaries: List[str]) -> str:
    """Reduce Step: Synthesizes intermediate chunk summaries into an executive briefing."""
    combined_notes = "\n\n".join(
        f"[Section {i+1} Takeaways]:\n{summary}" 
        for i, summary in enumerate(intermediate_summaries)
    )

    system_prompt = (
        "You are a Chief Technology Officer (CTO). "
        "Synthesize the following section summaries into a cohesive Master Executive Summary. "
        "Structure your response into:\n"
        "1. Executive Synthesis (1 concise narrative paragraph)\n"
        "2. Key Strategic Recommendations (2 actionable numbered points)\n"
        "Do not repeat section headers. Synthesize the big picture."
    )

    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": combined_notes}
        ],
        temperature=0.2,
        max_tokens=300
    )
    return res.choices[0].message.content.strip()


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 012: MAP-REDUCE SUMMARIZER [/]")
    console.print("[bold yellow]===========================================================[/]\n")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    model = "qwen/qwen3.8-27b"

    # Multi-section enterprise report
    report_text = """
SECTION 1: COMPUTE & HARDWARE INFRASTRUCTURE
During the third quarter of 2026, the engineering team successfully brought our new northern data center facility online, deploying an additional 1,024 NVIDIA Blackwell GPUs across high-speed InfiniBand fabrics. Power usage effectiveness (PUE) dropped to 1.12, setting an all-time company record for energy efficiency. Liquid cooling infrastructure was certified with zero thermal throttling incidents reported during continuous 99.9% compute utilization.

SECTION 2: INFERENCE ENGINE OPTIMIZATIONS
To combat memory pressure on our flagship LLM endpoints, the runtime systems team rolled out FP8 matrix quantization alongside speculative decoding algorithms. As a direct result, P99 time-to-first-token dropped by 38% across all commercial clusters, and peak throughput expanded from 280 tokens/second to 490 tokens/second per active stream. KV-cache memory pressure declined by 35%, enabling 4x longer conversation context windows without GPU out-of-memory errors.

SECTION 3: CLOUD OPEX AND FINANCIAL RECONCILIATION
From a financial perspective, gross infrastructure cloud spend rose 12% quarter-over-quarter to $4.2 million, driven primarily by physical hardware acquisition and long-term facility lease commitments. However, due to the inference efficiency gains introduced in Section 2, the unit cost per million tokens processed dropped precipitously by 28%. We anticipate breaking even on capital expenditure within four quarters as enterprise subscription volume continues to compound.
"""

    chunks = chunk_document(report_text, max_chunk_chars=750)
    console.print(f"[bold cyan]📄 Document partitioned into {len(chunks)} chunks for Map-Reduce processing.[/]\n")

    # MAP PHASE
    console.print("[bold yellow]⚙️  Executing MAP Phase (Local chunk summarization)...[/]")
    intermediate_summaries = []
    for i, chunk in enumerate(chunks):
        summary = map_summarize(client, model, chunk, i + 1, len(chunks))
        intermediate_summaries.append(summary)
        console.print(Panel(
            summary,
            title=f"📌 [bold green]Map Output (Chunk {i+1}/{len(chunks)})[/]",
            border_style="green"
        ))

    # REDUCE PHASE
    console.print("\n[bold magenta]⚡ Executing REDUCE Phase (Global executive synthesis)...[/]")
    executive_summary = reduce_synthesize(client, model, intermediate_summaries)

    console.print(Panel(
        f"[bold white]{executive_summary}[/]",
        title="🏆 [bold magenta]Consolidated Master Executive Summary[/]",
        border_style="magenta"
    ))


if __name__ == "__main__":
    main()
