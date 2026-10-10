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

---

## 🧩 Code Dissection: Why Did We Write It This Way?

For beginners reading [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/006-token-budget-calculator/main.py), here is why we used `tiktoken` and sub-word boundary decoding:

### 1. `tiktoken` vs. `len(text.split())`
```python
encoding = tiktoken.get_encoding("cl100k_base")
token_ids = encoding.encode(text)
num_tokens = len(token_ids)
```
* **Why did we write this?** To accurately measure the exact number of tokens the model engine will bill and process.
* **The Beginner Trap:** Writing `words = len(text.split())` and multiplying by 1.3 to guess token count.
* **Why guessing fails:** In source code, punctuation (`{`, `}`, `()`), and technical terminology (`torch.cuda.is_available()`), the character-to-token ratio changes dramatically. In Bengali or Japanese, a single word can be 5 tokens! `tiktoken` compiles OpenAI's BPE vocabulary in Rust, producing the exact ground truth count in microseconds.

---

### 2. Decoding Tokens Individually to Inspect Boundaries
```python
token_chunks = [encoding.decode([tid]) for tid in token_ids]
```
* **Why did we write this?** Passing an array with a single token ID `[tid]` into `encoding.decode()` reverses only that specific sub-word.
* **The Visual Insight:** It exposes the hidden space markers (e.g. `·engineering` vs `engineering`), showing beginners that whitespace is almost always fused into the subsequent token rather than existing as its own token.

---

### 3. Pre-Flight Budgeting in Production
* **Why run this before calling the API?**
  If a user uploads a 500-page document into a 32k context model, calling the API without pre-flight token counting results in:
  1. A wasted network connection.
  2. A failed `HTTP 400 ContextLengthExceeded` exception.
  Counting locally with `tiktoken` costs 0 dollars and 0 milliseconds, allowing you to reject, summarize, or chunk the document *before* failing.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Load Tokenizer Encoding:**
   ```python
   import tiktoken
   encoding = tiktoken.get_encoding("cl100k_base")
   ```
2. **Step 2: Tokenize and Map IDs:**
   ```python
   token_ids = encoding.encode(text)
   print("Token count:", len(token_ids))
   ```
3. **Step 3: Decode Chunks to Visualize Boundaries:**
   ```python
   token_chunks = [encoding.decode([tid]) for tid in token_ids]
   ```
4. **Step 4: Build a Multi-Model Pricing Matrix:**
   Create a table of pricing rates per million tokens and compute projected costs for high-scale request volumes.

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
