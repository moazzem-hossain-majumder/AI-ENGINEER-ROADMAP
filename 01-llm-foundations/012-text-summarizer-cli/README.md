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

---

## 🧩 Code Dissection: Why Did We Write It This Way?

For beginners reading [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/012-text-summarizer-cli/main.py), here is why we used paragraph-based chunking and two-stage Map-Reduce orchestration:

### 1. Paragraph-Aware Chunking vs. Naive Fixed Character Slicing
```python
paragraphs = text.strip().split("\n\n")
```
* **Why did we write this?** To preserve **semantic coherence**.
* **What could be written instead? (The Naive Way):**
  Beginners often slice strings by fixed character counts:
  `chunk = text[i : i + 1000]`
* **Why fixed slicing is broken:** It chops words directly in half (e.g. `in|frastructure` becomes two fragments) and severs sentences mid-thought. Splitting on double newlines `\n\n` guarantees that whole thoughts stay intact inside each chunk.

---

### 2. Map-Reduce vs. Stuffing the Whole Document into a 1M Context Window
* **The Question:** *"Models like Gemini 1.5/2.0 have a 1-million token context window. Why not just pass the whole 50-page document in one prompt?"*
* **The Problem:** **Attention Dilution**.
  When a model is given 500,000 tokens in a single prompt, the attention weights are spread paper-thin. Specific metrics (like *"PUE energy efficiency dropped to 1.12"*) get completely ignored in favor of generic summary statements.
* **Why Map-Reduce wins:** In the **Map step**, the model reads only 500 tokens. Its full attention capacity is focused on extracting exact metrics. The **Reduce step** then synthesizes these high-density bullet points into an executive brief with zero loss of critical detail.

---

### 3. Temperature Tuning: Map ($T=0.0$) vs. Reduce ($T=0.2$)
* **Map Phase ($T=0.0$):** Extraction must be strictly factual and deterministic. We want zero creative hallucinations when reading numbers and statistics.
* **Reduce Phase ($T=0.2$):** A tiny touch of temperature allows the model to smoothly synthesize the discrete notes into a natural, executive-level narrative flow without wandering off topic.

---

### 4. Alternative Summarization Patterns in Production
- **Refine Pattern:** The model summarizes Chunk 1. Then it takes Chunk 2 and refines its existing summary. Then Chunk 3. *Pros:* Constant memory. *Cons:* Sequential (cannot be parallelized across workers).
- **Hierarchical Tree Summarization:** Used for 1,000+ page documents: chunks are mapped, intermediate summaries are grouped into clusters and reduced, and the cluster summaries are reduced again.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Document Chunking:**
   Split the input text into a list of paragraphs bounded by a maximum character count.
2. **Step 2: Implement the Map Step (`map_summarize`):**
   Loop over each chunk and prompt the LLM to extract key facts.
3. **Step 3: Implement the Reduce Step (`reduce_synthesize`):**
   Combine the bullet points from all chunks into a final synthesis prompt.
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

📄 Document partitioned into 3 chunks for Map-Reduce processing.

⚙️  Executing MAP Phase (Local chunk summarization)...
┌───────────────────────── 📌 Map Output (Chunk 1/3) ─────────────────────────┐
│ *   Deployed 1,024 NVIDIA Blackwell GPUs on InfiniBand fabrics in a new     │
│ northern data center, achieving a record-low Power Usage Effectiveness      │
│ (PUE) of 1.12.                                                              │
│ *   Certified liquid cooling infrastructure maintained zero thermal         │
│ throttling incidents while sustaining 99.9% continuous compute utilization. │
└─────────────────────────────────────────────────────────────────────────────┘
┌───────────────────────── 📌 Map Output (Chunk 2/3) ─────────────────────────┐
│ *   Implementation of FP8 matrix quantization and speculative decoding      │
│ reduced P99 time-to-first-token by 38% and increased peak throughput from   │
│ 280 to 490 tokens/second per active stream.                                 │
│ *   KV-cache memory pressure decreased by 35%, allowing for 4x longer       │
│ conversation context windows without triggering GPU out-of-memory errors.   │
└─────────────────────────────────────────────────────────────────────────────┘
┌───────────────────────── 📌 Map Output (Chunk 3/3) ─────────────────────────┐
│ *   Gross infrastructure cloud spend increased 12% quarter-over-quarter to  │
│ $4.2 million, while the unit cost per million tokens processed decreased by │
│ 28% due to inference efficiency gains.                                      │
│ *   The organization anticipates breaking even on capital expenditure       │
│ within four quarters, driven by compounding enterprise subscription volume. │
└─────────────────────────────────────────────────────────────────────────────┘

⚡ Executing REDUCE Phase (Global executive synthesis)...
┌───────────────── 🏆 Consolidated Master Executive Summary ──────────────────┐
│ 1. Executive Synthesis                                                      │
│ Our infrastructure strategy has successfully decoupled scale from cost,     │
│ establishing a high-efficiency foundation that supports aggressive          │
│ performance gains.                                                          │
│                                                                             │
│ 2. Key Strategic Recommendations                                            │
│ 1. Accelerate Enterprise Onboarding to Capitalize on Unit Economics.        │
│ 2. Standardize and Scale the Optimized Inference Stack.                     │
└─────────────────────────────────────────────────────────────────────────────┘
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

1. **Hierarchical Summarization:** If a document is 500 pages, a single Reduce step might still overflow. How would you design a **Tree / Hierarchical Reduce** step?
2. **Custom Extraction Focus:** Alter the Map prompt to extract only financial numbers and risks, filtering out all operational commentary.
