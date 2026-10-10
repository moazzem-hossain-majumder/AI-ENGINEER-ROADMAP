# 🟢 Project 008: Chain-of-Thought (CoT) Reasoning

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Unlock advanced multi-step logic, math, and problem solving by forcing the model to generate intermediate reasoning tokens.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand why LLMs fail at multi-step arithmetic, logic, and planning when forced to answer directly.
2. Master the cognitive mechanics of **Chain-of-Thought (CoT)**: How generating intermediate reasoning tokens expands the model's effective computation budget.
3. Apply **Zero-Shot CoT** using directive triggers (`"Think step-by-step"`).
4. Implement **Structured Scratchpads** with `<thinking>` and `<answer>` XML tags.
5. Parse and isolate internal thoughts from user-facing answers using regex extraction.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
Direct Prompt (No CoT)  ➔ Hallucinates / Miscalculates due to 0 intermediate compute
Structured CoT Prompt   ➔ Emits <thinking> (Step-by-step scratchpad) ➔ Emits <answer> (Clean extracted solution)
```

1. **The Transformer Computation Limit:** A transformer predicts the next token in constant time per layer. For complex math or logic puzzles, it cannot compute 10 steps of mental arithmetic in a single forward pass without emitting intermediate tokens.
2. **Intermediate Scratchpad:** When prompted with `<thinking>...</thinking>`, each reasoning token emitted becomes part of the subsequent context window, allowing the self-attention mechanism to build on its own verified deduction steps.
3. **Structured Delimitation:** By forcing the model to separate its scratchpad into tags, your application can:
   - Display the reasoning chain to the user (transparency / auditability).
   - Or hide the internal reasoning and pass only the `<answer>` downstream to end users.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, you will see a comparison on a classic multi-step trick word problem:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 008: CHAIN-OF-THOUGHT      
===========================================================

🧩 Multi-Step Logic & Math Puzzle:
"A cloud server cluster has 12 nodes. Each node runs 8 virtual machines.
During morning peak, 25% of all VMs process database tasks, and half of the
remaining VMs run AI inference jobs. Each AI inference job requires 3 GPU cores.
How many GPU cores are needed in total?"

❌ Direct Answering (Prone to math & deduction mistakes):
Direct Guess: 108 GPU cores.

🧠 Chain-of-Thought (Step-by-Step Scratchpad):
┌────────────────────────── 💭 Internal Reasoning ──────────────────────────┐
│ 1. Total nodes = 12.                                                      │
│ 2. VMs per node = 8.                                                      │
│    Total VMs = 12 * 8 = 96 VMs.                                           │
│ 3. Database VMs = 25% of 96 = 24 VMs.                                     │
│ 4. Remaining VMs = 96 - 24 = 72 VMs.                                      │
│ 5. AI inference VMs = half of remaining = 72 / 2 = 36 VMs.                │
│ 6. GPU cores per AI job = 3 cores.                                        │
│    Total GPU cores = 36 * 3 = 108 cores.                                  │
└───────────────────────────────────────────────────────────────────────────┘

🎯 Verified Final Answer:
108 GPU cores
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/008-chain-of-thought/main.py).

Key snippet:
```python
prompt = f"""Solve this puzzle. You MUST structure your response into:
<thinking>
Step-by-step arithmetic and deduction steps.
</thinking>
<answer>
The final numerical answer with units.
</answer>

Puzzle: {puzzle}"""
```

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/008-chain-of-thought/main.py
```

---

## 🧪 Hands-On Experiments

1. **Try a Logic Riddle:** Replace the puzzle with a logic ordering problem (e.g., *"Alice is older than Bob, Charlie is younger than Alice but older than Bob..."*). Observe how CoT maps each relative age before concluding.
2. **Expose or Hide Thinking:** Modify the script to log the `<thinking>` trace to a file for audit trails while returning only `<answer>` to the console.
