# 🟢 Project 006: Token Budget & Cost Estimator

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Master sub-word tokenization with Byte Pair Encoding (BPE), context window budgeting, and multi-model cost modeling.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand why LLMs process **tokens** rather than raw characters or words.
2. Master **Byte Pair Encoding (BPE)** tokenization using `tiktoken`.
3. Visually inspect sub-word token boundaries and whitespace chunks.
4. Calculate pre-flight token budgets before making API calls to prevent context window overflow.
5. Model financial expenses across leading AI models (Groq Llama/Qwen, Google Gemini, OpenAI GPT-4o, Anthropic Claude).

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[Raw Input String] ➔ [BPE Tokenizer (tiktoken)] ➔ [Integer Token IDs] ➔ [Decoded Sub-word Chunks] ➔ [Multi-Model Cost Model]
```

1. **Tokenization (BPE):** Words are split into frequent sub-word statistical units (e.g., `tokenization` becomes `["token", "ization"]`). Punctuation and spaces are often bundled into neighboring tokens.
2. **Token ID Mapping:** Each token maps to a unique integer in the model's vocabulary (~100,000 to 200,000 IDs).
3. **Pre-flight Budgeting:** An AI engineer counts tokens locally *before* making network requests. If prompt tokens exceed the model's maximum allowed limit (e.g. 8k, 32k, 128k), the system truncates or compresses the text locally rather than paying for a failed API call.
4. **Financial Cost Modeling:** Inference providers charge per million tokens:
   $$\text{Total Cost} = \left(\frac{\text{Prompt Tokens}}{1,000,000} \times \text{Price}_{\text{in}}\right) + \left(\frac{\text{Completion Tokens}}{1,000,000} \times \text{Price}_{\text{out}}\right)$$

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, you will see visual token boundaries and a multi-model cost comparison table:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 006: TOKEN BUDGET & COST   
===========================================================

📝 Input Text:
'Artificial intelligence engineering requires mastering RAG, agent workflows, and cost management!'

🔍 Sub-word Token Breakdown:
[Art][ificial] [intelligence] [engineering] [requires] [mastering] [R]
[AG][,] [agent] [workflows][,] [and] [cost] [management][!]

📊 Tokenization Metrics:
┌────────────────────────────┬────────────────────┐
│ Metric                     │ Measurement        │
├────────────────────────────┼────────────────────┤
│ Total Characters           │ 98                 │
│ Total Words                │ 11                 │
│ Total Tokens               │ 16                 │
│ Characters Per Token       │ 6.1                │
└────────────────────────────┴────────────────────┘

💰 Cost Projection for 100,000 Requests (Assuming 16 prompt tokens + 250 completion tokens):
┌───────────────────────────┬──────────────┬──────────────┬───────────────┐
│ Model Provider            │ Prompt Cost  │ Output Cost  │ Total Cost    │
├───────────────────────────┼──────────────┼──────────────┼───────────────┤
│ Groq (Open Source / Qwen) │ $0.09        │ $1.98        │ $2.07         │
│ Google Gemini 1.5 Flash   │ $0.12        │ $7.50        │ $7.62         │
│ OpenAI GPT-4o-mini        │ $0.24        │ $15.00       │ $15.24        │
│ OpenAI GPT-4o             │ $4.00        │ $250.00      │ $254.00       │
└───────────────────────────┴──────────────┴──────────────┴───────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/006-token-budget-calculator/main.py).

Key snippet:
```python
import tiktoken

# Use standard modern OpenAI/Open-Source tokenizer encoding
encoding = tiktoken.get_encoding("cl100k_base")
tokens = encoding.encode("Artificial intelligence engineering")
print("Token Count:", len(tokens))
print("Token IDs:", tokens)
```

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/006-token-budget-calculator/main.py
```

---

## 🧪 Hands-On Experiments

1. **Test Code vs. Prose:** Pass a block of Python code vs an English paragraph of the same character length. Notice how code and symbols consume significantly more tokens per character.
2. **Test Non-English Text:** Enter a sentence in Bengali, Spanish, or Japanese. Notice that non-Latin scripts use more tokens per word due to UTF-8 byte fragmentation.
