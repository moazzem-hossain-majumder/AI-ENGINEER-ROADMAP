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

### 3. Terminal I/O Buffering & `sys.stdout.flush()`
A common bug when implementing streaming from scratch is calling `print(chunk, end="")` and seeing nothing appear until the entire generation finishes!
- **Why?** Operating system terminals buffer stdout to optimize CPU throughput. Small strings are stored in an internal buffer until a newline `\n` is encountered or the buffer fills.
- **The Fix:** Call `sys.stdout.write(chunk)` followed immediately by `sys.stdout.flush()`, forcing the operating system to paint each token to the screen the millisecond it arrives.

### 4. Key Production Telemetry Metrics
- **TTFT (Time-to-First-Token):** Time elapsed between dispatching the prompt and receiving the very first delta token:
  $$\text{TTFT} = t_{\text{first\_token}} - t_{\text{start}}$$
- **TPS (Tokens Per Second):** The inference engine's raw generation speed:
  $$\text{TPS} = \frac{\text{Chunks Streamed}}{t_{\text{end}} - t_{\text{first\_token}}}$$

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Start High-Precision Timer:**
   Use `start_time = time.perf_counter()` (preferred over `time.time()` for microsecond accuracy).
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
   Calculate TTFT, generation duration, and tokens per second, and present the results in a summary table.

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
In production AI applications, the time it takes for a Large Language Model (LLM) to generate a full response can range from several seconds to minutes. Without streaming, users are forced to wait for the entire output before seeing any result, leading to high bounce rates and frustration. Streaming delivers tokens (words or characters) as they are generated, providing immediate visual feedback. This reduces the *perceived* latency, making the application feel instantaneous and responsive, which is critical for retaining user engagement.

2. **Network Efficiency and Resource Optimization**
Streaming leverages asynchronous communication protocols, such as Server-Sent Events (SSE) or WebSockets, rather than blocking HTTP requests. This allows the server to maintain a lightweight, persistent connection and push data incrementally. Consequently, the client does not need to buffer large payloads, and the server can manage concurrent connections more efficiently without holding open heavy request slots. This architecture scales better under high traffic loads, as it prevents network timeouts and reduces the memory footprint on both the client and server sides.

3. **Real-Time Interactivity and Error Handling**
Streaming enables real-time user interactions that are impossible with batch responses. Users can stop the generation mid-stream if the output is incorrect or irrelevant, saving computational resources and API costs. Additionally, if a network error or server-side failure occurs, the application can gracefully handle the partial response or retry the request without losing the entire context.

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
