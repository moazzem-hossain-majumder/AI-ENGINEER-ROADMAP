# 🟢 Project 014: Error Handling, Exponential Backoff & Provider Fallback

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Build resilient production AI pipelines that survive rate limits (429), timeouts, and provider outages.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand common production API failure modes: HTTP 429 (Rate Limits), HTTP 503 (Capacity Overload), and socket timeouts.
2. Implement **Exponential Backoff with Jitter** to prevent the "Thundering Herd" retry storm.
3. Architect **Multi-Provider Fallback (Circuit Breaker)**: Automatically fail over from **Groq** to **Google Gemini** if the primary provider fails.
4. Distinguish between transient errors (safe to retry) and fatal errors (never retry, e.g., HTTP 401 Invalid Key, HTTP 400 Context Exceeded).

---

## 📚 Background Knowledge & Theory (Read Before Coding)

To build enterprise-grade AI software that maintains 99.9% uptime, you must design for transient failures.

### 1. Why Do AI APIs Fail Frequently?
Unlike traditional web servers that return static database records in 5 milliseconds, LLM inference runs on shared GPU/LPU hardware clusters under extreme variable load:
- **HTTP 429 (Rate Limit Exceeded):** Providers enforce strict requests-per-minute (RPM) and tokens-per-minute (TPM) limits. Spikes in concurrent traffic trigger instant 429 errors.
- **HTTP 503 / 500 (Service Unavailable / Overloaded):** GPUs run out of memory (OOM) or clusters queue requests until timeouts expire.
- **High Latency Variance:** P99 response times can spike from 500ms to 20 seconds during peak cloud hours.

### 2. The Danger of Naive Immediate Retries (Thundering Herd)
If 100 concurrent users hit a rate limit and your code immediately retries `while True: call()`, all 100 clients hammer the server at the exact same microsecond:
- This is known as a **Retry Storm** or **Thundering Herd Problem**.
- It worsens the provider's overload and causes your API key to be temporarily banned.

### 3. The Mathematics of Exponential Backoff with Jitter
Pioneered by Amazon AWS and Google SRE, the standard solution is **Truncated Exponential Backoff with Full Jitter**:

$$t_{\text{sleep}} = \text{random}(0, \min(T_{\max}, T_{\text{base}} \times 2^{\text{attempt}}))$$

```
Attempt 1 Fail ──➔ Sleep ~0.5s to 1.0s
Attempt 2 Fail ──➔ Sleep ~1.0s to 2.0s
Attempt 3 Fail ──➔ Sleep ~2.0s to 4.0s
```

Adding random "jitter" spreads out concurrent retries evenly across time, breaking up the synchronization of incoming traffic.

### 4. Resilient Multi-Provider Fallback Architecture
For mission-critical applications, relying on a single AI provider is a single point of failure (SPOF).
A production AI gateway maintains a primary and secondary provider:

```
[User Request]
       │
       ▼
[Attempt Primary Provider: Groq] ──(Success)──➔ [Return Result]
       │ (Fails after 2 retries / 429 / 503)
       ▼
[Log Failover Warning]
       │
       ▼
[Attempt Secondary Provider: Gemini] ──(Success)──➔ [Return Result]
       │ (Fails)
       ▼
[Graceful Error Report to User]
```

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Classify Exceptions (Retryable vs. Non-Retryable):**
   - Retryable: `RateLimitError` (429), `APITimeoutError`, `InternalServerError` (500/503).
   - Non-Retryable: `AuthenticationError` (401), `BadRequestError` (400 - bad prompt).
2. **Step 2: Implement Jittered Backoff Function:**
   ```python
   def sleep_with_jitter(attempt: int, base: float = 0.5, max_sleep: float = 5.0):
       max_delay = min(max_sleep, base * (2 ** attempt))
       delay = random.uniform(0.5, max_delay)
       time.sleep(delay)
   ```
3. **Step 3: Build Resilient Caller with Multi-Provider Fallback:**
   - Try Primary Provider (Groq) up to `max_retries`.
   - If Groq fails with an unrecoverable or exhausted retry error, immediately catch and switch to Secondary Provider (Gemini).
4. **Step 4: Simulate Failure to Test Resilience:**
   Trigger an intentional simulated failure (such as an invalid model name or forced rate limit) and observe how the system seamlessly falls back to Gemini without crashing.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[Request Prompt] ➔ [Try Primary (Groq)] ➔ [If Retryable Error: Backoff + Jitter] ➔ [If Primary Exhausted: Switch to Gemini] ➔ [Deliver Answer]
```

1. **Primary Dispatch:** System attempts generation via Groq for ultra-low latency.
2. **Backoff Loop:** If a transient network glitch occurs, backoff pauses with random jitter.
3. **Graceful Failover:** If Groq remains unreachable, the fallback router invokes Google Gemini transparently.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, you will see normal operation followed by a simulated primary outage failover:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 014: RESILIENT RETRY & FALLBACK
===========================================================

Scenario 1: Normal Primary Execution (Groq)
┌─────────────────────── 🚀 Primary Provider Success ────────────────────────┐
│ Provider: Groq Cloud (Model: qwen/qwen3.8-27b)                             │
│ Output: Exponential backoff prevents retry storms by spreading retries     │
│ across randomized intervals.                                               │
│ Latency: 0.42s | Status: 200 OK                                            │
└────────────────────────────────────────────────────────────────────────────┘

Scenario 2: Primary Outage Simulation ➔ Automatic Fallback to Google Gemini
[Primary Alert] Groq failed: Simulated 503 Provider Outage.
[Retry Attempt 1] Applying exponential backoff: sleeping 0.82s...
[Primary Alert] Groq failed again: Primary provider unavailable.
[Failover Triggered] 🔄 Switching to Secondary Provider: Google Gemini...
┌─────────────────────── 🌟 Secondary Provider Fallback ─────────────────────┐
│ Provider: Google Gemini (Model: gemini-3.8-flash)                          │
│ Output: An AI fallback router guarantees high availability by routing      │
│ around outages to alternative LLM APIs.                                    │
│ Latency: 1.05s | Status: 200 OK (Recovered via Fallback)                   │
└────────────────────────────────────────────────────────────────────────────┘

✔ Resilience Verification: Pipeline survived primary outage with zero user downtime!
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/014-error-handling-retry/main.py).

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/014-error-handling-retry/main.py
```

---

## 🧪 Hands-On Experiments

1. **Tune Backoff Rates:** Change `base_delay` from 0.5s to 2.0s and observe how long the system pauses between simulated errors.
2. **Circuit Breaker Threshold:** Implement a counter so that after 5 consecutive failures, the router stays on the secondary provider for 60 seconds before trying the primary again.
