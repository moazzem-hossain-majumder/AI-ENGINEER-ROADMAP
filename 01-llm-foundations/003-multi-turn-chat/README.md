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

## 📚 Background Knowledge & Theory (Read Before Coding)

To build a conversational chatbot from scratch, you must understand state management in distributed AI systems.

### 1. The Fundamental Statelessness of LLM APIs
When you interact with an LLM via HTTP POST requests, the remote cluster operates like a pure mathematical function.
- It **does not store** your user ID, your previous questions, or session cookies in model memory.
- Every HTTP connection is completely independent.
- If you ask *"What is my name?"* in Turn 2 without providing Turn 1, the model literally has zero access to past tokens.

### 2. The Illusion of Memory: Client-Side Context Re-Injection
To create a conversational experience, the **client application** must maintain an append-only memory buffer of all previous turns and resend the entire conversation on every single request:

```text
Turn 1 Request: [User: "I am Moazzem"]
Turn 1 Response: [Assistant: "Hi Moazzem"]

Turn 2 Request: [User: "I am Moazzem", Assistant: "Hi Moazzem", User: "What is my name?"]
Turn 2 Response: [Assistant: "Your name is Moazzem"]
```

### 3. The Quadratic Cost & Context Limit Problem
Because the conversation history is resent on every turn:
- **Token consumption grows quadratically**: In an $N$-turn dialogue, total prompt tokens scale as $O(N^2)$.
- **Context limit overflow**: Once the accumulated token count exceeds the model's context limit (e.g. 8k, 32k, or 128k tokens), the API will reject your request with an `HTTP 400 ContextWindowExceeded` error.

### 4. Memory Strategies in Production AI
To solve context explosion, AI engineers use three primary buffer strategies:
1. **Sliding Window Buffer (This Project):** Retains only the last $K$ turns. The system prompt is pinned at index `0`, while turns older than $K$ are discarded.
2. **Conversation Summary Memory:** When history exceeds a threshold, an LLM call summarizes older turns into a single paragraph.
3. **Vector/Episodic Memory (Phase 2 & 5):** Turns are embedded into a vector database and retrieved semantically when relevant.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Design the `ChatSession` Class:**
   - Store `self.history: List[Dict[str, str]] = []`.
   - Store `self.system_prompt: str`.
   - Store `self.max_turns: int = 5`.
2. **Step 2: Implement Payload Construction (`_build_payload`):**
   - Calculate maximum messages to keep: `max_messages = self.max_turns * 2`.
   - Slice the tail: `trimmed = self.history[-max_messages:]`.
   - Return `[{"role": "system", "content": self.system_prompt}] + trimmed`.
3. **Step 3: Implement Message Transmission (`send_message`):**
   - Append user query: `self.history.append({"role": "user", "content": text})`.
   - Call API with `messages=self._build_payload()`.
   - Extract reply and append: `self.history.append({"role": "assistant", "content": reply})`.
4. **Step 4: Build the Interactive CLI Loop:**
   - Run an infinite `while True` loop listening to `console.input()`.
   - Handle custom commands: `/history`, `/clear`, `/exit`.
   - Gracefully catch `KeyboardInterrupt` (Ctrl+C).

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
User Input ➔ Append to History ➔ Trim Old Messages (Sliding Window) ➔ Prepend System Prompt ➔ Send Full Array ➔ Store Assistant Reply
```

1. **Client-Side State Storage:** The `ChatSession` class maintains an internal Python list `self.history = []`.
2. **Conversation Append:** When you ask a question, `{"role": "user", "content": "..."}` is added to the list.
3. **Sliding Window Truncation:** To prevent token limit errors, the app limits the buffer to the last $N$ turns.
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
