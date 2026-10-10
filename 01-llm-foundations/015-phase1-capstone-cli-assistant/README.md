# 🏆 Project 015: Phase 1 Capstone: Universal CLI AI Copilot

> **Phase 01: LLM Foundations & Prompt Engineering (CAPSTONE)**  
> *The ultimate synthesis of Projects 001–014: A production-ready, resilient, multi-provider terminal AI Copilot.*

---

## 🎯 Learning Outcomes
By completing this Capstone project, you will:
1. Synthesize all core LLM concepts from Phase 01 into an integrated, production-grade application:
   - **Multi-Provider Resilience (001, 014):** Groq primary with automatic Google Gemini failover.
   - **Sampling & Determinism (002):** Configurable temperature and max tokens.
   - **Stateful Memory (003):** Sliding window buffer with session persistence.
   - **Structured Outputs (004):** Pydantic-validated session analytics and exports.
   - **Low-Latency Streaming (005):** Real-time token streaming with live TTFT and tokens/sec telemetry.
   - **Token Economics (006):** Real-time BPE token tracking and live dollar spend calculation.
   - **Dynamic Personas (011):** On-the-fly persona switching (`/persona mentor`, `coder`, `eli5`).
   - **Prompt Defense (010):** Pre-flight adversarial pattern scanning and XML boundary sandboxing.
2. Build an extensible architecture ready for real-world daily productivity.

---

## 📚 Background Knowledge & Theory (Read Before Coding)

To build a professional AI copilot from scratch, you must understand end-to-end system orchestration.

### 1. The Capstone Architecture
A production copilot is an orchestration engine that unifies multiple subsystems into an interactive loop:

```
                      ┌──────────────────────────────────────────────┐
                      │             User Terminal Prompt             │
                      └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    Layer 1: Prompt Injection Guardrail       │
                      │  (Regex Scanner + <user_prompt> Sandboxing)  │
                      └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    Layer 2: Memory & Context Assembler       │
                      │  (Active Persona + Pinned System + Window)   │
                      └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    Layer 3: Resilient Inference Dispatch     │
                      │  (Groq SSE Streaming ➔ Gemini Fallback)      │
                      └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    Layer 4: Telemetry & Token Accounting     │
                      │  (TTFT, Tokens/sec, tiktoken Cost Tracking)  │
                      └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    Layer 5: Structured Persistence & Export  │
                      │  (Pydantic V2 Session Export: JSON/Markdown) │
                      └──────────────────────────────────────────────┘
```

### 2. State & Buffer Isolation
The `CopilotEngine` maintains clean separation between:
- **Session Identity:** Unique session ID and start timestamp.
- **Active Persona:** The currently loaded system prompt instructions.
- **Conversation Buffer:** List of preceding (user, assistant) message turns.
- **Financial Ledger:** Cumulative prompt and completion token counters.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Session & Ledger Models:**
   Define a Pydantic model `SessionReport` to track message count, total tokens, estimated cost, and exportable chat history.
2. **Step 2: Guardrail & Delimiter Sanitizer:**
   Embed the heuristic regex scanner and wrap user queries inside `<user_query>` tags.
3. **Step 3: Multi-Provider Streaming Engine:**
   Attempt real-time streaming via Groq. If Groq triggers a timeout or connection failure, catch the exception, announce the failover, and stream from Google Gemini.
4. **Step 4: Interactive Command Router:**
   Listen for special slash commands:
   - `/persona [name]`: Switch persona dynamically (`mentor`, `coder`, `eli5`).
   - `/cost`: Print token count and total dollar spend.
   - `/history`: Print memory buffer table.
   - `/clear`: Wipe memory.
   - `/export`: Export session to a Markdown/JSON file.
   - `/exit`: Terminate session.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

1. **Startup:** Initializes Groq and Gemini clients, sets default persona (`mentor`), and opens conversation buffer.
2. **Query Processing:** Scans for injection attacks, constructs the context array, and streams tokens live.
3. **Telemetry & Budgeting:** Calculates TTFT and tokens/sec, updates the cumulative session cost ledger.
4. **Session Export:** On demand, serializes conversation history into structured files.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you launch `main.py`, you enter the interactive Copilot environment:

```text
======================================================================
  🤖 UNIVERSAL AI COPILOT (PHASE 01 CAPSTONE)                         
  Provider: Groq Cloud (Auto-failover: Gemini) | Persona: mentor      
======================================================================

Commands: /persona [name], /cost, /history, /clear, /export, /exit

You > What is a vector embedding?

[Streaming response live...]
A vector embedding is a way of translating complex human concepts—words,
sentences, or images—into a list of numbers (a vector) that a computer
can understand. Words with similar meanings end up close together in
this mathematical space, allowing algorithms to search by meaning rather
than exact keywords!

  [Telemetry: 284.1 ms TTFT | 492.3 tokens/sec | Model: qwen/qwen3.8-27b]

You > /persona coder
[Persona Updated] 💻 Active Persona: Staff Software Engineer

You > How do we index them for sub-10ms search?

[Streaming response live...]
In production, flat brute-force scanning doesn't scale past 100k vectors.
We use Hierarchical Navigable Small World (HNSW) graphs combined with
Scalar Quantization (SQ8) to achieve logarithmic-time graph traversal
and 75% memory compression...

  [Telemetry: 312.4 ms TTFT | 488.1 tokens/sec | Model: qwen/qwen3.8-27b]

You > /cost
┌───────────────────────────┬────────────────────┐
│ Session Telemetry Metric  │ Value              │
├───────────────────────────┼────────────────────┤
│ Total Messages            │ 4                  │
│ Total Prompt Tokens       │ 142                │
│ Total Completion Tokens   │ 218                │
│ Estimated Session Spend   │ $0.000048          │
└───────────────────────────┴────────────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/015-phase1-capstone-cli-assistant/main.py).

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/015-phase1-capstone-cli-assistant/main.py
```

*(Or to run an automated end-to-end self-test without typing, run: `python main.py --test`)*

---

## 🧪 Hands-On Experiments

1. **Test Auto-Failover Live:** Temporarily corrupt your `GROQ_API_KEY` in `.env` and chat with the copilot. Watch it instantly fail over to Google Gemini without interrupting your session!
2. **Add a Custom Persona:** Open `main.py` and register a new persona (e.g. `interviewer` or `pirate`).
3. **Export Your Session:** Have a 5-turn chat and type `/export`. Open the generated `session_export.json` file to inspect your session history.
