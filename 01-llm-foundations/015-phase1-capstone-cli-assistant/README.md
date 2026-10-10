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

---

## 🧩 Code Dissection: Why Did We Write It This Way?

For beginners reading [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/015-phase1-capstone-cli-assistant/main.py), here is how the architectural subsystems connect together:

### 1. The `CopilotEngine` Orchestrator
```python
class CopilotEngine:
    def __init__(self, default_persona: str = "mentor", max_turns: int = 6):
        self.session_id = f"copilot-{int(time.time())}"
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
```
* **Why did we write this?** Instead of writing loose functions, an engine class holds the entire state machine:
  - Conversation buffer (`self.history`)
  - Token ledger (`self.total_prompt_tokens`, `self.total_completion_tokens`)
  - Active persona configuration (`self.active_persona_key`)
  - API provider instances (`Groq` and `genai`)

---

### 2. Real-Time Token Accounting with `tiktoken` During Streaming
```python
p_tokens = len(self.tokenizer.encode(user_query))
self.total_prompt_tokens += p_tokens
...
c_tokens = len(self.tokenizer.encode(final_reply))
self.total_completion_tokens += c_tokens
```
* **Why did we write this?** When streaming responses over HTTP SSE (`stream=True`), some provider engines do not emit final token usage objects in the stream delta chunks.
* **The Solution:** By passing the final concatenated reply through local Rust-based `tiktoken`, the copilot computes exact token counts and live dollar spend locally with zero reliance on missing stream metadata.

---

### 3. Structured Export via Pydantic (`SessionExport`)
```python
report = SessionExport(
    session_id=self.session_id,
    active_persona=self.active_persona_key,
    total_turns=len(turns),
    estimated_cost_usd=self.get_estimated_cost(),
    history=turns
)
```
* **Why export to JSON?** In enterprise AI engineering, saving raw chat logs into structured, typed JSON files is the prerequisite for:
  - Building offline evaluation benchmarks (Phase 06).
  - Fine-tuning dataset curation (Phase 07).
  - Tracing and observability in Datadog, Langfuse, or LangSmith.

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
   - `/persona [name]`: Switch persona dynamically.
   - `/cost`: Print token count and total dollar spend.
   - `/history`: Print memory buffer table.
   - `/clear`: Wipe memory.
   - `/export`: Export session to a JSON file.
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

You > How do we query them with HNSW?

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

### Mode 1: Automated Self-Test (Fastest)
```powershell
.\.venv\Scripts\python 01-llm-foundations/015-phase1-capstone-cli-assistant/main.py --test
```

### Mode 2: Interactive Terminal Chat
```powershell
.\.venv\Scripts\python 01-llm-foundations/015-phase1-capstone-cli-assistant/main.py
```

---

## 🧪 Hands-On Experiments

1. **Test Auto-Failover Live:** Temporarily corrupt your `GROQ_API_KEY` in `.env` and chat with the copilot. Watch it instantly fail over to Google Gemini without interrupting your session!
2. **Add a Custom Persona:** Open `main.py` and register a new persona (e.g. `interviewer` or `pirate`).
3. **Export Your Session:** Have a 5-turn chat and type `/export`. Open the generated `session_export.json` file to inspect your session history.
