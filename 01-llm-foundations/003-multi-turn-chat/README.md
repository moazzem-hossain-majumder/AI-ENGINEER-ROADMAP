# 🟢 Project 003: Multi-Turn Chat & Context Buffer

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Master conversational memory, the stateless nature of LLMs, and sliding window buffers.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand why LLMs are **fundamentally stateless**: The server does NOT remember you between requests.
2. Build an append-only conversation history array: `[system, user, assistant, user, assistant...]`.
3. Implement a **Sliding Window Buffer** to avoid overflowing the model's context window limit.
4. Build an interactive CLI chatbot with session controls (`/history`, `/clear`, `/exit`).

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
User Input ➔ Append to History ➔ Trim Old Messages (Sliding Window) ➔ Prepend System Prompt ➔ Send Full Array ➔ Store Assistant Reply
```

1. **Client-Side State Storage:** The `ChatSession` class maintains an internal Python list `self.history = []`.
2. **Conversation Append:** When you ask a question, `{"role": "user", "content": "..."}` is added to the list.
3. **Sliding Window Truncation:** To prevent token limit errors and skyrocketing API bills, the app limits the buffer to the last $N$ turns (e.g. `self.history[-10:]`).
4. **Context Injection:** The system prompt is always pinned at index `0`. The API receives the full list of preceding conversation turns.
5. **Memory Recall:** Because earlier turns are included in the prompt, the model can synthesize information from past answers seamlessly.

---

## 📸 Sample Terminal Output & Run Walkthrough

### 1. Automated Demonstration Mode:
Running `python main.py` runs a 3-turn demonstration proving fact storage and memory recall:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 003: MULTI-TURN CHAT BOT   
===========================================================

🤖 Running Multi-Turn Demonstration Scenario...

User (Turn 1): Hi! Remember that my favorite programming language is Rust.
AI:
Got it! I've noted that your favorite programming language is Rust. Let me know
if you have any questions or need help with it!

User (Turn 2): What is the capital of Japan?
AI:
The capital of Japan is Tokyo.

User (Turn 3): Based on our conversation earlier, what is my favorite 
programming language?
AI:
Your favorite programming language is Rust.

                   📜 Current Context Buffer (Memory State)                    
┌──────────┬──────────────┬───────────────────────────────────────────────────┐
│ Turn #   │ Role         │ Snippet                                           │
├──────────┼──────────────┼───────────────────────────────────────────────────┤
│ 0        │ system       │ You are a helpful, concise AI study tutor.        │
│ (Pinned) │              │ Remember all fact...                              │
│ 1        │ user         │ Hi! Remember that my favorite programming         │
│          │              │ language is Rust....                              │
│ 2        │ assistant    │ Got it! I've noted that your favorite programming │
│          │              │ language i...                                     │
│ 3        │ user         │ What is the capital of Japan?...                  │
│ 4        │ assistant    │ The capital of Japan is Tokyo....                 │
│ 5        │ user         │ Based on our conversation earlier, what is my     │
│          │              │ favorite progr...                                 │
│ 6        │ assistant    │ Your favorite programming language is Rust....    │
└──────────┴──────────────┴───────────────────────────────────────────────────┘

Tip: Run with --interactive or -i to chat live in the terminal!
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/003-multi-turn-chat/main.py).

---

## 🚀 How to Run and Check

### Mode A: Automated Self-Test (Fastest)
```powershell
.\.venv\Scripts\python 01-llm-foundations/003-multi-turn-chat/main.py
```

### Mode B: Interactive Terminal Chat
Chat with the model in real time:
```powershell
.\.venv\Scripts\python 01-llm-foundations/003-multi-turn-chat/main.py --interactive
```
*(In interactive mode, type `/history` to inspect memory, `/clear` to reset, or `/exit` to quit).*

---

## 🧪 Hands-On Experiments

1. **Verify Context Pruning:** Open [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/003-multi-turn-chat/main.py) and change `max_turns = 1`. Run the demo again and observe how Turn 1 is forgotten because the window slid past it!
2. **Experiment with Custom Personas:** Change `system_prompt` to act as a strict code auditor or interviewer.
