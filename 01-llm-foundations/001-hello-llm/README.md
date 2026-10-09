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

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[1. Load .env] ➔ [2. Initialize Client] ➔ [3. Format Messages Array] ➔ [4. HTTP POST] ➔ [5. Parse Metadata & Display]
```

1. **Environment Initialization:** The script loads `GROQ_API_KEY` and `GEMINI_API_KEY` securely from the project `.env` file without exposing tokens in source code.
2. **Message Packaging:** The prompt is converted into standard OpenAI-compatible role objects:
   - `system`: Governs how the LLM should think and respond (e.g. mentor persona, maximum length constraints).
   - `user`: Contains the prompt query.
3. **Model Processing:** The model generates output tokens sequentially until reaching an end-of-sequence token (`stop`) or hitting the `max_tokens` token ceiling.
4. **Metadata Extraction:** The returned payload contains the textual output plus runtime telemetries:
   - `choices[0].message.content`: The textual answer.
   - `choices[0].finish_reason`: Indicates whether the output concluded normally (`stop`) or was truncated (`length`).
   - `usage`: Exact count of tokens processed for budgeting and latency calculations.

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

Key snippet:
```python
response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[
        {"role": "system", "content": "You are an encouraging, world-class AI mentor."},
        {"role": "user", "content": "What is the single most important skill for an AI Engineer in 2026?"}
    ],
    temperature=0.7,
    max_tokens=150
)
```

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
