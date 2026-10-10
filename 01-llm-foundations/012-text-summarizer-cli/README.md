# 🟢 Project 012: Map-Reduce Chunked Text Summarizer

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Summarize massive documents that exceed context limits using the two-stage Map-Reduce pattern.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand the **"Lost in the Middle"** phenomenon in transformer attention windows.
2. Master the **Map-Reduce Summarization Architecture**:
   - **Chunk:** Partition large documents into semantic chunks.
   - **Map:** Summarize each chunk independently to capture localized facts.
   - **Reduce:** Synthesize the collection of intermediate summaries into an executive briefing.
3. Overcome context length limits and minimize prompt attention dilution.
4. Build a modular CLI document summarizer.

---

## 📚 Background Knowledge & Theory (Read Before Coding)

To process enterprise documents (annual reports, clinical trials, codebases), you must understand document decomposition patterns.

### 1. The "Lost in the Middle" Phenomenon
Even when models support 128k or 1M token context windows, empirical research (Liu et al., Stanford 2023) shows that transformers do not attend evenly across large contexts:
- Recall accuracy is highest at the **first 10%** and **last 10%** of the prompt (Primacy and Recency effects).
- Key facts buried in the middle are frequently missed or forgotten.
- Shoving an entire 50-page PDF into a single prompt results in vague, superficial summaries.

### 2. The Map-Reduce Pattern
Borrowed from distributed computing (Dean & Ghemawat, Google 2004), the **Map-Reduce pattern** decomposes large-scale summarization into two distinct phases:

```
[Massive Document: 50 Pages]
         │
         ├── Split into Chunks ──➔ [Chunk 1]  [Chunk 2]  [Chunk 3]
         │                              │          │          │
         ├── MAP STEP (Individual LLM)  ▼          ▼          ▼
         │                         [Summary 1] [Summary 2] [Summary 3]
         │                              │          │          │
         └── REDUCE STEP (Synthesis)    └──────────┬──────────┘
                                                   ▼
                                     [Master Executive Summary]
```

1. **Map Step:** Each chunk is summarized independently. Because each chunk is short (e.g. 500 to 1,000 tokens), the model's full attention capacity is focused on extracting every critical detail, statistic, and key decision without attention dilution.
2. **Reduce Step:** The intermediate summaries are combined into a consolidated prompt. The LLM synthesizes them into a unified, high-level briefing with overall themes and action items.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Document Chunking:**
   Split the input text into a list of paragraphs or chunks bounded by a maximum character/token count:
   ```python
   def chunk_text(text: str, max_chunk_chars: int = 1500) -> List[str]:
       # Split on paragraph boundaries '\n\n' to preserve semantic integrity
   ```
2. **Step 2: Implement the Map Step (`map_summarize`):**
   Loop over each chunk and prompt the LLM:
   *"Extract key facts, statistics, and takeaways from this section in 2 bullet points."*
3. **Step 3: Implement the Reduce Step (`reduce_synthesize`):**
   Combine the bullet points from all chunks into a final synthesis prompt:
   *"Synthesize these section summaries into a cohesive Executive Summary with key strategic action items."*
4. **Step 4: Output the Multi-Stage Pipeline:**
   Print intermediate chunk summaries followed by the final consolidated briefing.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[Raw Long Document] ➔ [Paragraph Chunking] ➔ [Parallel Map LLM Calls] ➔ [Collect Intermediate Summaries] ➔ [Final Reduce Call] ➔ [Master Executive Brief]
```

1. **Document Loading:** The long document is segmented at paragraph breaks.
2. **Map Processing:** Each segment is distilled into concise takeaways.
3. **Reduce Synthesis:** Intermediate notes are synthesized into an overarching executive summary.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, you will see the multi-stage summarization pipeline execute live:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 012: MAP-REDUCE SUMMARIZER 
===========================================================

📄 Document Loaded: Quarterly AI Infrastructure Report (3 Chunks, 950 words)

⚙️ Running MAP Phase: Summarizing individual sections...
┌── 📌 Map Step (Chunk 1/3: Compute Cluster Expansion) ──┐
│ • Added 1,024 H100 GPUs across northern data centers.  │
│ • PUE energy efficiency improved to 1.14.              │
└────────────────────────────────────────────────────────┘
┌── 📌 Map Step (Chunk 2/3: Model Inference Latency) ────┐
│ • P99 latency dropped by 38% via speculative decoding. │
│ • KV-cache memory pressure reduced via FP8 quantization│
└────────────────────────────────────────────────────────┘
┌── 📌 Map Step (Chunk 3/3: Financials & Cloud Opex) ────┐
│ • Cloud inference compute spend rose 12% to $4.2M.     │
│ • Unit cost per 1M tokens processed dropped by 28%.    │
└────────────────────────────────────────────────────────┘

⚡ Running REDUCE Phase: Synthesizing master executive summary...
┌─────────────── 🏆 Consolidated Master Executive Summary ───────────────┐
│ Executive Takeaway:                                                    │
│ Q3 delivered significant infrastructure expansion alongside aggressive │
│ efficiency gains. Despite total compute spend rising 12% to $4.2M due  │
│ to the deployment of 1,024 H100s, unit costs per million tokens dropped│
│ by 28% and P99 latency decreased by 38% through speculative decoding   │
│ and FP8 quantization.                                                  │
│                                                                        │
│ Strategic Recommendations:                                             │
│ 1. Accelerate FP8 rollout across remaining inference endpoints.        │
│ 2. Continue hardware expansion in energy-efficient data centers.       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/012-text-summarizer-cli/main.py).

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/012-text-summarizer-cli/main.py
```

---

## 🧪 Hands-On Experiments

1. **Hierarchical Summarization:** If a document is 500 pages, a single Reduce step might still overflow. How would you design a **Tree / Hierarchical Reduce** step? *(Hint: Group summaries in batches of 5, reduce each batch, then reduce the batch summaries).*
2. **Custom Extraction Focus:** Alter the Map prompt to extract only financial numbers and risks, filtering out all operational commentary.
