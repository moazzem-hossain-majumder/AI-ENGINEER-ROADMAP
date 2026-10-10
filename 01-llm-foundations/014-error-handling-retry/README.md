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

---

## 🧩 Code Dissection: Why Did We Write It This Way?

For beginners reading [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/014-error-handling-retry/main.py), here is why jittered backoff and multi-provider fallback routing were engineered:

### 1. Exponential Backoff with "Full Jitter"
```python
def calculate_jittered_backoff(attempt: int, base: float = 0.5, max_sleep: float = 4.0):
    calculated_ceiling = min(max_sleep, base * (2 ** attempt))
    delay = random.uniform(base, calculated_ceiling)
    return delay
```
* **Why did we write this?** To prevent the **Thundering Herd Problem** (Retry Storm).
* **What could be written instead? (The Beginner Trap):**
  Writing deterministic backoff: `time.sleep(2 ** attempt)`.
* **Why static backoff fails:** If 1,000 users hit a rate limit at 12:00:00, with static backoff all 1,000 clients sleep for *exactly 2.000 seconds* and all 1,000 clients hammer the server at *exactly 12:00:02*! The server immediately crashes again. Adding `random.uniform()` spreads the retries out across time.

---

### 2. Multi-Provider Fallback Router (Circuit Breaker)
```python
try:
    result = call_primary_groq(prompt)
except Exception:
    result = call_secondary_gemini(prompt)
```
* **Why did we write this?** To eliminate the Single Point of Failure (SPOF).
* **The Business Impact:** Cloud providers frequently have 15-minute regional outages or API degradation. If your startup relies on a single provider, your product is down. By catching primary exhaustion and failing over to Google Gemini, your app maintains 99.99% uptime with zero user interruption.

---

### 3. Production Gateway Alternatives in the Industry
- **LiteLLM (`pip install litellm`):** A popular open-source proxy that translates any LLM call into a standardized format and includes built-in load-balancing and fallback routing.
- **Portkey / Cloudflare AI Gateway:** Managed enterprise proxies that provide caching, rate-limit management, and multi-provider failover at the DNS layer.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Classify Exceptions (Retryable vs. Non-Retryable):**
   - Retryable: `RateLimitError` (429), `APITimeoutError`, `InternalServerError` (500/503).
   - Non-Retryable: `AuthenticationError` (401), `BadRequestError` (400 - bad prompt).
2. **Step 2: Implement Jittered Backoff Function:**
   Calculate dynamic delay using exponential power and random uniform scaling.
3. **Step 3: Build Resilient Caller with Multi-Provider Fallback:**
   - Try Primary Provider (Groq) up to `max_retries`.
   - If Groq fails with an unrecoverable error, immediately catch and switch to Secondary Provider (Gemini).
4. **Step 4: Simulate Failure to Test Resilience:**
   Trigger an intentional simulated failure and observe how the system seamlessly falls back to Gemini without crashing.

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

Scenario 1: Normal Primary Execution (Groq Cloud)
┌─────────────────────── 🚀 Primary Provider Succeeded ───────────────────────┐
│ Exponential backoff prevents API retry storms by progressively increasing   │
│ the delay between consecutive retry attempts.                               │
│                                                                             │
│ Provider: Groq Cloud | Latency: 0.56s | Status: 200 OK                      │
└─────────────────────────────────────────────────────────────────────────────┘

Scenario 2: Primary Outage Simulation ➔ Automatic Failover to Gemini
  ↳ [Primary: Groq] Attempting request (outage simulated)...
  ⚠️ [Primary Glitch]: NotFoundError. Applying backoff: sleeping 0.50s (Attempt 1/2)...
  ⚠️ [Primary Glitch]: NotFoundError. Applying backoff: sleeping 0.59s (Attempt 2/2)...
  ❌ [Primary Exhausted]: Retries failed. Initiating circuit failover.
  🔄 [Fallback Router]: Routing to Secondary Provider: Google Gemini...
┌───────────────── 🌟 Secondary Provider Fallback Succeeded ──────────────────┐
│ Exponential backoff prevents retry storms by progressively increasing the   │
│ wait time between failed attempts, which spreads out traffic spikes.        │
│                                                                             │
│ Provider: Google Gemini (Fallback) | Latency: 1.05s | Status: Recovered     │
└─────────────────────────────────────────────────────────────────────────────┘

✔ Resilience Verification Complete: System maintained 100% uptime through 
multi-provider routing!
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
