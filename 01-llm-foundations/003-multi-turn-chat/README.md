# 🟢 Project 003: Multi-Turn Chat & Context Buffer

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Master conversational memory, the stateless nature of LLMs, and sliding window buffers.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand why LLMs are **fundamentally stateless**: The server does NOT remember you between requests.
2. Build an append-only conversation history array: `[system, user, assistant, user, assistant...]`.
3. Implement a **Sliding Window Buffer** to avoid overflowing the model's context window limit.
4. Build an interactive CLI chatbot with session controls (`/history`, `/clear`, `/tokens`, `/exit`).

---

## 📖 Concept Explanation: Why LLMs Have No Memory

A common misconception for beginners is that when you chat with an AI, the model "remembers" what you said earlier.

In reality:
```
Turn 1:
You: "My name is Moazzem."
Payload Sent: [ {"role": "user", "content": "My name is Moazzem."} ]
LLM Replies: "Nice to meet you, Moazzem!"

Turn 2:
You: "What is my name?"
If you send ONLY: [ {"role": "user", "content": "What is my name?"} ]
LLM Replies: "I don't know your name because you haven't told me."
```

To give the illusion of memory, the **client application** must store the full message array and resend the entire history on every single turn:

```
Turn 2 (Corrected):
Payload Sent: [
    {"role": "system", "content": "You are a helpful tutor."},
    {"role": "user", "content": "My name is Moazzem."},
    {"role": "assistant", "content": "Nice to meet you, Moazzem!"},
    {"role": "user", "content": "What is my name?"}
]
LLM Replies: "Your name is Moazzem!"
```

### The Trade-off: Context Window & Cost Explosion
Because you re-send past tokens every turn:
- **Cost grows quadratically** if conversations are long.
- **Context limit reached**: When messages exceed the model's maximum context length.

### The Solution: Sliding Window Buffer
Keep the `system` message pinned at index 0, and retain only the last $N$ turns (e.g., last 6 exchanges), discarding older turns when the buffer overflows.

---

## 💻 What the Code Does (`main.py`)

1. Manages a `ChatSession` class with:
   - `system_message`: Pinned instructions.
   - `messages`: List of message objects.
   - `max_turns`: Maximum history turns to keep.
2. Provides an interactive terminal chat interface.
3. Built-in CLI commands:
   - `/history`: Inspect raw message JSON array sent to the API.
   - `/clear`: Reset conversation state.
   - `/exit` or `/quit`: Exit chat.

---

## 🚀 How to Run

```bash
.\.venv\Scripts\python 01-llm-foundations/003-multi-turn-chat/main.py
```

---

## 🧪 Hands-On Experiments

1. **Test Memory:** Tell the bot: *"Remember the secret code: PHOENIX-99."* Then ask 2 unrelated questions. Then ask: *"What was the secret code?"*
2. **Buffer Pruning:** Set `max_turns = 2` in `main.py`. Have a 5-turn conversation and ask about Turn 1. Notice how older messages fall out of the context window.
