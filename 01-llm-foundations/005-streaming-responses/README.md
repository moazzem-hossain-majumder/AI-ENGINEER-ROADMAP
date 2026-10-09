# 🟢 Project 005: Streaming & Real-Time Token Delivery

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Master low-latency streaming responses, Server-Sent Events (SSE), and Time-to-First-Token (TTFT).*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand why waiting for an entire generation (Blocking/Unary) hurts User Experience (UX).
2. Measure and optimize **Time-to-First-Token (TTFT)** vs. total generation latency.
3. Stream LLM tokens in real time using `stream=True` and iterator chunks.
4. Calculate generation throughput in **Tokens per Second (TPS)**.
5. Build an interactive terminal typewriter assistant.

---

## 📖 Concept Explanation: Blocking vs. Streaming

### Unary (Blocking) Request
The user waits in silence while the model generates all 300 tokens on the GPU cluster. Only when the final token finishes does the HTTP response return.
* *Perceived latency:* High (3 to 6 seconds of frozen blank screen).

```
User Prompt ──➔ [ Server generates token 1, 2, 3 ... 300 ] ──➔ Whole text returned at once
```

### Streaming (Server-Sent Events - SSE)
The connection stays open as an HTTP event stream. As soon as the GPU produces token 1, it is immediately flushed across the network wire to the client.
* *Perceived latency:* Instantaneous (<150ms TTFT).

```
User Prompt ──➔ Token 1 ──➔ Token 2 ──➔ Token 3 ──➔ ... (Live typing animation)
```

### Key Production Metrics for AI Engineers
* **TTFT (Time-to-First-Token):** Time between sending the prompt and receiving the very first chunk.
* **TPS (Tokens Per Second):** Generation speed of the model engine (`total_tokens / streaming_duration`).

---

## 💻 What the Code Does (`main.py`)

1. Sends a generation request with `stream=True`.
2. Measures TTFT precision with high-resolution timers (`time.perf_counter()`).
3. Flushes each token chunk directly to the terminal stdout in real-time.
4. Computes and displays real-time performance analytics:
   - Time-to-First-Token
   - Tokens per Second (Throughput)
   - Total elapsed time

---

## 🚀 How to Run

```bash
.\.venv\Scripts\python 01-llm-foundations/005-streaming-responses/main.py
```

---

## 🧪 Hands-On Experiments

1. **Compare Models:** In `main.py`, compare the TTFT and tokens/sec between `qwen/qwen3.8-27b` and `openai/gpt-oss-20b`.
2. **Buffer Stream:** Try buffering 3 tokens before rendering. When would token buffering be useful in production? *(Hint: Markdown parsing, code formatting, or safety scanning).*
