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

## 📚 Background Knowledge & Theory (Read Before Coding)

To build streaming applications from scratch, you must understand low-latency HTTP transport and Python generator streams.

### 1. The Perceived Latency Problem
Autoregressive generation is computationally intensive. A model generating a 400-word response might take 3 to 6 seconds on GPU infrastructure:
- **Unary/Blocking Mode:** The client sends an HTTP request and waits in complete silence. The user stares at a loading spinner for 5 seconds. To the user, the app feels broken or sluggish.
- **Streaming Mode:** As soon as token #1 is predicted on the server (~200ms), it is pushed across the wire. The user starts reading immediately. To the human eye, reading speed is roughly 5 to 8 words per second. Even if the full generation takes 5 seconds, the application feels instantaneous!

### 2. Under the Hood: Server-Sent Events (SSE)
When you set `stream=True`, the client sends an HTTP request with header `Accept: text/event-stream`.
- Instead of closing the HTTP connection with a single JSON payload, the connection remains open.
- The server pushes incremental chunks over HTTP using the Server-Sent Events (SSE) format:
  ```text
  data: {"choices": [{"delta": {"content": "Artificial"}}]}
  data: {"choices": [{"delta": {"content": " intelligence"}}]}
  data: [DONE]
  ```
- The Python SDK client parses these lines on-the-fly and yields them as a Python generator (`for chunk in stream:`).

---

## 🧩 Code Dissection: Why Did We Write It This Way?

For beginners reading [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/005-streaming-responses/main.py), here is why specific low-level Python I/O and timing methods were chosen:

### 1. `time.perf_counter()` vs. `time.time()`
```python
start_time = time.perf_counter()
```
* **Why did we write this?** `time.perf_counter()` accesses the CPU's high-resolution monotonic performance counter with sub-microsecond precision.
* **What could be written instead?** `time.time()`.
* **Why `time.time()` is flawed for benchmarks:** `time.time()` measures calendar wall-clock time. If the operating system synchronizes its clock via NTP (Network Time Protocol) or daylight savings shifts during your request, `time.time()` can produce negative or erratic durations. `perf_counter()` is mathematically guaranteed to only tick forward.

---

### 2. `sys.stdout.write()` and `sys.stdout.flush()` vs. `print()`
```python
sys.stdout.write(content_piece)
sys.stdout.flush()
```
* **Why did we write this?** Operating systems buffer terminal text to optimize system calls. If you write small token fragments, the OS holds them in RAM until a newline `\n` arrives.
* **The Beginner Mistake:** Writing `print(content_piece, end="")`.
  - In Python, `print(..., end="")` does NOT flush the buffer. Text appears frozen, then suddenly bursts onto the screen all at once when the stream closes!
  - `sys.stdout.flush()` (or `print(..., end="", flush=True)`) forces the operating system to paint each token to the screen the exact millisecond it arrives over the network.

---

### 3. `delta.content` vs. `message.content`
```python
delta = chunk.choices[0].delta
content_piece = delta.content or ""
```
* **Why did we write this?** In streaming mode, the server sends a **delta** (a differential change) containing only the newly generated token chunk, not the entire message so far.
* **Watch out for `None`:** The very final chunk of a stream often contains `delta.content = None` along with `finish_reason = "stop"`. Writing `delta.content or ""` defends against `TypeError: write() argument must be str, not None`.

---

### 4. Architectural Alternatives: SSE vs. WebSockets
- **Server-Sent Events (SSE - Used here):** One-way streaming from server to client over standard HTTP. Lightweight, firewall-friendly, and standard for LLMs.
- **WebSockets:** Full-duplex two-way communication. Necessary only if the user needs to interrupt the model with real-time microphone audio while it is speaking.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Start High-Precision Timer:**
   Use `start_time = time.perf_counter()`.
2. **Step 2: Dispatch Request with `stream=True`:**
   ```python
   stream = client.chat.completions.create(
       model="qwen/qwen3.8-27b",
       messages=[...],
       stream=True
   )
   ```
3. **Step 3: Loop Over Delta Chunks:**
   ```python
   for chunk in stream:
       content_piece = chunk.choices[0].delta.content or ""
       if content_piece:
           if first_token_time is None:
               first_token_time = time.perf_counter()
           sys.stdout.write(content_piece)
           sys.stdout.flush()
   ```
4. **Step 4: Compute & Display Telemetry:**
   Calculate TTFT, generation duration, and tokens per second.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[Prompt Sent] ➔ [HTTP Streaming Connection Opens] ➔ [First Token Emitted (TTFT Recorded)] ➔ [Delta Chunks Streamed Live] ➔ [Stream Closes & Telemetry Displayed]
```

1. **HTTP Streaming Connection:** Setting `stream=True` instructs the server to transmit data via Server-Sent Events (SSE).
2. **High-Resolution Telemetry:** We record `start_time = time.perf_counter()`.
3. **Chunk Iteration:** As each chunk arrives, `delta.content` is extracted and instantly flushed to standard output (`sys.stdout.flush()`).
4. **TTFT Calculation:** The moment the first non-empty token arrives, `first_token_time` is recorded.
5. **Throughput Calculation:** We measure `tokens_per_sec = chunks_received / generation_duration`.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, the answer types itself out in real-time on your screen, followed by a telemetry table:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 005: TOKEN STREAMING       
===========================================================

Prompt: Why is streaming critical when building production AI web applications?

Streaming output live...

1. **Perceived Latency and User Experience**
In production AI applications, the time it takes for a Large Language Model (LLM) to generate a full response can range from several seconds to minutes. Without streaming, users are forced to wait for the entire output before seeing any result, leading to high bounce rates and frustration. Streaming delivers tokens as they are generated, providing immediate visual feedback. This reduces the *perceived* latency, making the application feel instantaneous and responsive.

2. **Network Efficiency and Resource Optimization**
Streaming leverages asynchronous communication protocols, such as Server-Sent Events (SSE) or WebSockets, rather than blocking HTTP requests. This allows the server to maintain a lightweight, persistent connection and push data incrementally.

         ⚡ Streaming Performance Telemetry          
┌────────────────────────────────┬──────────────────┐
│ Metric                         │ Measurement      │
├────────────────────────────────┼──────────────────┤
│ Model                          │ qwen/qwen3.8-27b │
│ Time-to-First-Token (TTFT)     │ 318.9 ms         │
│ Total Generation Time          │ 0.95 s           │
│ Chunks / Tokens Streamed       │ 300              │
│ Generation Speed               │ 478.1 tokens/sec │
└────────────────────────────────┴──────────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/005-streaming-responses/main.py).

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/005-streaming-responses/main.py
```

---

## 🧪 Hands-On Experiments

1. **Test Prompt Variations:** Change the prompt in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/005-streaming-responses/main.py) to ask for code or poetry and observe how TTFT and tokens/sec vary.
2. **Observe Network Speeds:** Compare running against Groq (`qwen/qwen3.8-27b`) versus other models to see the raw hardware inference speed differences.
