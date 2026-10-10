# 🟢 Project 001: Hello LLM (Anatomy of an LLM API Call)

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *The simplest, most fundamental building block of AI engineering: your first API call.*

---

## 🎯 Learning Outcomes
By the end of this project, you will:
1. Understand how an AI Engineer interacts with Large Language Models via APIs.
2. Know the exact structure of an LLM request payload (`model`, `messages`, `role`).
3. Understand the roles: `system`, `user`, and `assistant`.
4. Inspect and interpret response metadata (`prompt_tokens`, `completion_tokens`, `finish_reason`).
5. Execute requests using **Groq** (ultra-fast inference) and switch seamlessly to **Google Gemini**.

---

## 📚 Background Knowledge & Theory (Read Before Coding)

To build this project from scratch, you must understand the underlying computer science and architecture behind Large Language Model APIs.

### 1. What is an LLM Under the Hood?
A Large Language Model (such as Llama, Qwen, or GPT) is an **autoregressive transformer decoder**. 
- It does **not** "think" or "search Google" by default.
- It is a mathematical function that calculates probability distributions over a fixed vocabulary of tokens:
  
  $$P(w_t \mid w_1, w_2, \dots, w_{t-1})$$

Given a sequence of input tokens, it predicts the single most probable next token, appends it to the sequence, and repeats this cycle until it outputs an `<end_of_sequence>` token.

### 2. Why Do We Use Cloud Inference APIs?
Running modern models locally requires immense hardware:
- A 70-Billion parameter model stored in 16-bit floating point precision requires **~140 GB of high-bandwidth GPU VRAM** (equivalent to two $30,000 NVIDIA H100 GPUs).
- Inference providers like **Groq** run these models on custom LPU (Language Processing Unit) hardware or clustered enterprise GPUs, exposing access via standardized HTTP REST APIs.

### 3. The OpenAI Chat Completions Standard
In modern AI engineering, the `/chat/completions` specification created by OpenAI has become the universal industry standard. Providers including **Groq, Anthropic (via adapters), DeepSeek, Together AI, Mistral, and local engines like Ollama and vLLM** all implement this exact same Python interface:
```python
client.chat.completions.create(model=..., messages=[...])
```
Learning this API once allows you to target almost every model provider on Earth.

---

## 🧩 Code Dissection: Why Did We Write It This Way?

For beginners reading [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/001-hello-llm/main.py), here is the exact purpose behind every architectural decision, what could be written instead, and the trade-offs:

### 1. Loading Secrets via `dotenv`
```python
load_dotenv(root_dir / ".env")
api_key = os.getenv("GROQ_API_KEY")
```
* **Why did we write this?** Security. It keeps your credentials in a local `.env` file that is ignored by Git.
* **What could be written instead?**
  - *Naive Way:* `api_key = "gsk_sZVXxFj79sWY..."` (Hardcoding).
  - *Why you should NEVER do that:* Automated GitHub crawlers scrape public repos every second. If an API key is committed, it is compromised, revoked, or exploited within minutes.
* **Production Alternative:** For production cloud deployments (AWS, GCP, Kubernetes), keys are injected via environment secret vaults (e.g., AWS Secrets Manager, HashiCorp Vault) rather than `.env` files.

---

### 2. The `Groq` Client vs. Raw HTTP Requests
```python
client = Groq(api_key=api_key)
response = client.chat.completions.create(...)
```
* **Why did we write this?** The official SDK wraps HTTP network calls into clean Python objects, handles connection reuse (HTTP Keep-Alive), serializes payloads, and deserializes JSON responses automatically.
* **What could be written instead? (The Raw Alternative):**
  You could write pure Python using the `requests` library without installing `groq`:
  ```python
  import requests
  headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
  payload = {
      "model": "qwen/qwen3.8-27b",
      "messages": [{"role": "user", "content": "Hello!"}]
  }
  res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload).json()
  answer = res["choices"][0]["message"]["content"]
  ```
* **Why the SDK wins:** SDKs handle automatic exponential retries on 429 rate limits, socket timeouts, and type safety autocomplete in modern IDEs.

---

### 3. The Messages List Structure (`role` and `content`)
```python
messages = [
    {"role": "system", "content": "You are a concise mentor."},
    {"role": "user", "content": "Explain what an AI engineer does."}
]
```
* **Why did we write this?** Modern LLMs are trained on **ChatML** templates. The `system` message conditions the model's persona and constraints before it ever reads the user's prompt.
* **What could be written instead?**
  In older models (like GPT-3 `text-davinci-003`), prompts were a single raw string:
  ```python
  prompt = "System: You are a mentor.\nUser: Explain what an AI engineer does.\nAssistant:"
  ```
* **Why the list of roles wins:** Modern models use special internal boundary tokens (e.g. `<|im_start|>system...<|im_end|>`). Passing explicit role dictionaries ensures the provider formats these boundary tokens with 100% mathematical accuracy.

---

### 4. Windows UTF-8 Terminal Reconfiguration
```python
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
```
* **Why did we write this?** Default Windows PowerShell / Command Prompt uses the legacy `cp1252` encoding. Printing modern emojis (`🚀`, `🤖`, `📊`) causes Python on Windows to crash with `UnicodeEncodeError`.
* **What could be written instead?** Avoiding emojis entirely or forcing users to type `chcp 65001` in terminal before running Python.
* **Why this wins:** Makes scripts work out-of-the-box on any Windows machine without requiring manual terminal configuration.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

If you are opening an empty `main.py` file to write this yourself:

1. **Step 1: Manage Secrets Safely:**
   Never hardcode API keys. Install `python-dotenv` and load keys using `os.getenv("GROQ_API_KEY")`.
2. **Step 2: Initialize the Client:**
   Import `from groq import Groq` and initialize `client = Groq(api_key=api_key)`.
3. **Step 3: Structure the Message Payload:**
   Construct a list of dictionaries where each item has `"role"` and `"content"`.
4. **Step 4: Execute the Request:**
   Call `client.chat.completions.create(model=..., messages=..., temperature=0.7, max_tokens=150)`.
5. **Step 5: Extract the Results & Telemetry:**
   - Text output: `response.choices[0].message.content`
   - Finish reason: `response.choices[0].finish_reason`
   - Token statistics: `response.usage.prompt_tokens` and `response.usage.completion_tokens`

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[1. Load .env] ➔ [2. Initialize Client] ➔ [3. Format Messages Array] ➔ [4. HTTP POST] ➔ [5. Parse Metadata & Display]
```

1. **Environment Initialization:** The script loads `GROQ_API_KEY` and `GEMINI_API_KEY` securely from the project `.env` file without exposing tokens in source code.
2. **Message Packaging:** The prompt is converted into standard OpenAI-compatible role objects.
3. **Model Processing:** The model generates output tokens sequentially until reaching an end-of-sequence token (`stop`) or hitting the `max_tokens` token ceiling.
4. **Metadata Extraction:** The returned payload contains the textual output plus runtime telemetries.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you run `main.py`, here is the exact formatted visual output you will see in your terminal:

```text
====================================================
  AI ENGINEER ROADMAP - PROJECT 001: HELLO LLM     
====================================================

┌─────────────────── 🚀 Project 001: Outgoing API Request ────────────────────┐
│ Provider: Groq Cloud                                                        │
│ Model: qwen/qwen3.8-27b                                                     │
│ System Prompt: You are an encouraging, world-class AI engineering mentor.   │
│ Keep your response strictly under 2 sentences.                              │
│ User Prompt: What is the single most important skill for an AI Engineer in  │
│ 2026?                                                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────── 🤖 Model Response ─────────────────────────────┐
│ The single most important skill is the ability to design robust, scalable   │
│ systems that effectively orchestrate and evaluate LLMs in production. This  │
│ requires a deep understanding of both the probabilistic nature of AI models │
│ and the rigorous engineering principles needed to ensure reliability and    │
│ cost-efficiency.                                                            │
└─────────────────────────────────────────────────────────────────────────────┘

          📊 Request Execution Metadata          
┌────────────────────────────┬──────────────────┐
│ Metric                     │ Value            │
├────────────────────────────┼──────────────────┤
│ Model Used                 │ qwen/qwen3.8-27b │
│ Finish Reason              │ stop             │
│ Prompt Tokens (Input)      │ 55               │
│ Completion Tokens (Output) │ 55               │
│ Total Tokens               │ 110              │
│ Latency                    │ 0.46 seconds     │
└────────────────────────────┴──────────────────┘

Testing Google Gemini Provider...
┌───────────────────────── 🌟 Google Gemini Response ─────────────────────────┐
│ A token is a basic unit of text—typically a word or piece of a word—that an │
│ LLM uses to process and generate language.                                  │
│                                                                             │
│ Latency: 1.15s | Model: gemini-3.8-flash                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/001-hello-llm/main.py).

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/001-hello-llm/main.py
```

---

## 🧪 Hands-On Experiments (Try These!)

1. **Change the system prompt:** Open [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/001-hello-llm/main.py), change `"You are an encouraging mentor"` to `"You are a pirate who explains tech concepts in pirate slang"`. Observe how the response tone changes.
2. **Inspect token count:** Ask a 1-word question (`"Hi"`) vs a 50-word question. Notice how `Prompt Tokens (Input)` scales linearly with the input length.
3. **Switch models:** Try changing `model_name = "openai/gpt-oss-20b"` or `"allam-2-7b"` and observe latency and response differences.
