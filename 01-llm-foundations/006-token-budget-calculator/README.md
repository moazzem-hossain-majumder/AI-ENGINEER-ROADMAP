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

## 📚 Background Knowledge & Theory (Read Before Coding)

To manage LLM performance and cloud costs effectively, you must understand tokenization algorithms and cost economics.

### 1. Why Don't LLMs Process Characters or Words?
In natural language processing, there are three theoretical ways to represent text:
- **Character-level:** Sequences are too long. A 1,000-word essay would be ~6,000 individual characters, blowing through the transformer's attention window ($O(N^2)$ complexity).
- **Word-level:** The vocabulary is virtually infinite. New slang, typos, technical terms (e.g., `LangChain`, `PyTorch`), and non-English words would trigger missing word errors (`<UNK>`).
- **Sub-word Level (Byte Pair Encoding - BPE):** The sweet spot. Common words become single tokens (e.g., `"the"`, `"cat"`), while rare or composite words are broken down into sub-word pieces (e.g., `"tokenization"` $\to$ `["token", "ization"]`).

### 2. How Byte Pair Encoding (BPE) Works
Originally a data compression algorithm (Gage, 1994), BPE is the standard tokenization method for modern LLMs (GPT-4, Llama 3, Qwen):
1. The vocabulary starts with individual base bytes (UTF-8).
2. The training corpus is scanned for the most frequent adjacent character pairs (e.g., `'t'` and `'h'`).
3. These pairs are merged into a new single token (`'th'`).
4. This merge process repeats iteratively hundreds of thousands of times until the target vocabulary size (~100,000 to 200,000 tokens) is reached.
5. Leading spaces and punctuation are often fused into the beginning of words (e.g., `"·artificial"`).

### 3. The Token-to-Word Ratio & Language Disparity
- **English Prose:** On average, 1,000 English words correspond to **~1,333 tokens** (~0.75 words per token).
- **Source Code:** High punctuation and indentation create more tokens: 1,000 lines of code can consume **2,500+ tokens**.
- **Non-Latin Scripts (Bengali, Hindi, Arabic, Japanese):** Because these scripts require 3 or 4 UTF-8 bytes per character, a single non-Latin word may split into 3 to 6 sub-word tokens, making non-English processing more expensive and slower unless using a multilingual vocabulary like Qwen or Llama 3.

### 4. Financial Economics of LLM APIs
Production APIs bill separately for inputs and outputs:
- **Prompt (Input) Tokens:** Cheaper because processing prompt tokens can be parallelized across GPU matrix cores simultaneously during pre-fill.
- **Completion (Output) Tokens:** 2x to 5x more expensive because each token must be generated sequentially (one step at a time), bottlenecking GPU memory bandwidth.

$$\text{Total Cost} = \left(\frac{\text{Prompt Tokens}}{10^6} \times \text{Price}_{\text{in}}\right) + \left(\frac{\text{Completion Tokens}}{10^6} \times \text{Price}_{\text{out}}\right)$$

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Load Tokenizer Encoding:**
   ```python
   import tiktoken
   # cl100k_base is the standard modern tokenizer (used by GPT-4 and compatible models)
   encoding = tiktoken.get_encoding("cl100k_base")
   ```
2. **Step 2: Tokenize and Map IDs:**
   ```python
   token_ids = encoding.encode(text)
   print("Token count:", len(token_ids))
   ```
3. **Step 3: Decode Chunks to Visualize Boundaries:**
   To see where each token starts and ends, decode each integer ID individually:
   ```python
   token_chunks = [encoding.decode([tid]) for tid in token_ids]
   ```
4. **Step 4: Build a Multi-Model Pricing Matrix:**
   Create a table of pricing rates per million tokens and compute projected costs for high-scale request volumes (e.g. 50,000 daily queries).

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[Raw Input String] ➔ [BPE Tokenizer (tiktoken)] ➔ [Integer Token IDs] ➔ [Decoded Sub-word Chunks] ➔ [Multi-Model Cost Model]
```

1. **Tokenization (BPE):** Words are split into frequent sub-word statistical units.
2. **Token ID Mapping:** Each token maps to a unique integer in the model's vocabulary.
3. **Pre-flight Budgeting:** An AI engineer counts tokens locally *before* making network requests.
4. **Financial Cost Modeling:** Calculates projected dollar cost per million tokens across models.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, you will see visual token boundaries and a multi-model cost comparison table:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 006: TOKEN BUDGET & COST   
===========================================================

┌─────────────────────────────── 📝 Input Text ───────────────────────────────┐
│ Artificial intelligence engineering requires mastering RAG architectures,   │
│ autonomous agent loops, and rigorous token budget management.               │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────── 🔍 Sub-word Token Chunks (Colored Boundaries) ───────────────┐
│ [Art][ificial][·intelligence][·engineering][·requires][·mastering][·R][AG][ │
│ ·architectures][,][·autonomous][·agent][·loops][,][·and][·rigorous][·token] │
│ [·budget][·management][.]                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
         📊 Tokenization Metrics          
┌──────────────────────────┬─────────────┐
│ Metric                   │ Value       │
├──────────────────────────┼─────────────┤
│ Total Characters         │ 135         │
│ Total Words              │ 15          │
│ Total Tokens             │ 20          │
│ Avg Characters per Token │ 6.75        │
│ Encoding Standard        │ cl100k_base │
└──────────────────────────┴─────────────┘
                 💰 Cost Projection for 50,000 API Requests                  
         (Assuming 20 prompt tokens + 250 output tokens per request)         
┌──────────────────────────────────┬─────────────┬─────────────┬────────────┐
│ Model Provider                   │ Prompt Cost │ Output Cost │ Total Cost │
├──────────────────────────────────┼─────────────┼─────────────┼────────────┤
│ Groq Cloud (qwen/qwen3.8-27b)    │ $0.09       │ $2.00       │ $2.09      │
│ Google Gemini 1.5 Flash          │ $0.07       │ $3.75       │ $3.83      │
│ OpenAI GPT-4o-mini               │ $0.15       │ $7.50       │ $7.65      │
│ OpenAI GPT-4o                    │ $2.50       │ $125.00     │ $127.50    │
│ Anthropic Claude 3.5 Sonnet      │ $3.00       │ $187.50     │ $190.50    │
└──────────────────────────────────┴─────────────┴─────────────┴────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/006-token-budget-calculator/main.py).

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
