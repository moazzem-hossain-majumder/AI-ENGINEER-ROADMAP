# 🟢 Project 007: Few-Shot In-Context Learning

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Teach LLMs specialized domain classification and syntax through demonstration examples without weight fine-tuning.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand **In-Context Learning (ICL)**: How LLMs infer task patterns on-the-fly without gradient weight updates.
2. Recognize when **Zero-Shot** fails and why **Few-Shot** provides dramatic consistency gains.
3. Structure canonical `Input ➔ Output` demonstration pairs for high reliability.
4. Build an enterprise Customer Support Ticket Classifier that categorizes Intent, Sentiment, and SLA Priority.
5. Compare Zero-Shot vs. Few-Shot performance on ambiguous inputs.

---

## 📚 Background Knowledge & Theory (Read Before Coding)

To build robust classifiers without fine-tuning, you must understand the science of In-Context Learning.

### 1. What is In-Context Learning (ICL)?
Discovered prominently with GPT-3 (Brown et al., 2020), **In-Context Learning** is an emergent capability of large transformers:
- The model's weights ($\theta$) remain 100% frozen. No gradient descent, backpropagation, or training occurs.
- Instead, the transformer's **induction heads** (attention head circuits) detect statistical patterns across the demonstration pairs in the prompt context and dynamically map inputs to outputs.
- In effect, the model "learns" the task temporarily inside its activation layers during the forward pass.

### 2. Zero-Shot vs. Few-Shot vs. Fine-Tuning
| Technique | Weight Updates? | Setup Time | Cost | Best Used For |
|---|---|---|---|---|
| **Zero-Shot** | No | Seconds | Lowest | General knowledge, open-ended writing |
| **Few-Shot (ICL)** | No | Minutes | Low (slightly longer prompt) | Enterprise taxonomies, custom formats, specialized classification |
| **Fine-Tuning** | Yes | Hours / Days | High (training & hosting compute) | Teaching entirely new languages, extreme latency optimization |

### 3. Why Zero-Shot Fails in Production Classification
When prompted with *"Classify this ticket"*, the model has thousands of possible synonyms in its vocabulary:
- It might output `"Billing & Payment Problem"`, while your database schema requires `BILLING_DISPUTE`.
- It might include conversational commentary: *"I would classify this as an urgent issue because..."*
- Zero-Shot lacks the inductive bias needed for strict machine-to-machine data contracts.

### 4. Known Biases in Few-Shot Prompting (Watch Out!)
Research by Zhao et al. (2021) revealed three major biases when designing few-shot prompts:
1. **Majority Label Bias:** If 4 of your 5 examples demonstrate `TECHNICAL_OUTAGE`, the model will over-predict that label on ambiguous inputs. *Always balance your classes!*
2. **Recency Bias:** The model pays disproportionate attention to the final example in the prompt. Place your most representative example last.
3. **Delimiter Inconsistency:** Using different formats between examples confuses the model. Keep the delimiter syntax (`Ticket:`, `Output:`, `---`) strictly uniform.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Define the Closed Taxonomy:**
   Decide the exact enumerated values your enterprise software expects:
   - `Intent: [TECHNICAL_OUTAGE | BILLING_DISPUTE | FEATURE_REQUEST | ACCOUNT_ACCESS]`
   - `Priority: [P1_CRITICAL | P2_HIGH | P3_NORMAL]`
2. **Step 2: Construct Balanced Canonical Examples:**
   Write 3 to 4 distinct examples covering different classes, each showing:
   - Realistic input variation
   - Exact output key-value formatting
3. **Step 3: Build the Prompt Assembler:**
   Append the unseen test ticket to the bottom of the prompt and leave the output field open for completion (`Ticket: "{unseen_ticket}"\nOutput:`).
4. **Step 4: Execute at Zero Temperature:**
   Set `temperature=0.0` to ensure greedy decoding follows the established pattern deterministically.
5. **Step 5: Parse Key-Value Pairs:**
   Split the output lines on `:` and populate structured dictionaries or tables.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[System Persona] + [Few-Shot Demonstrations (Ex 1, 2, 3)] + [Unseen Test Query] ➔ [Consistent, Schema-Compliant Output]
```

1. **Zero-Shot Limitation:** Unconstrained classification results in inconsistent schemas and conversational ramblings.
2. **In-Context Conditioning:** 3 to 5 curated examples prime the attention heads to adhere strictly to the target taxonomy.
3. **Inference Execution:** The model completes the established pattern on the unseen test input.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, the system compares Zero-Shot vs. Few-Shot outputs on ambiguous tickets:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 007: FEW-SHOT PROMPTING    
===========================================================

┌──────────────────── 🎫 Incoming Customer Support Ticket ────────────────────┐
│ We lost all access to our production database immediately after renewing    │
│ our annual enterprise billing contract this morning! Fix this immediately,  │
│ our business is halted!                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
┌────────── ❌ Zero-Shot Output (Unpredictable Structure & Labels) ───────────┐
│ **Category:** Billing & Access / Account Management                         │
│ **Urgency:** Critical (P1)                                                  │
│                                                                             │
│ **Reasoning:**                                                              │
│ *   **Category:** The issue is directly linked to a billing action          │
│ (renewing the contract) resulting in a loss of access.                      │
└─────────────────────────────────────────────────────────────────────────────┘
┌────────────── ✅ Few-Shot Output (Strict Enterprise Taxonomy) ──────────────┐
│ Intent: TECHNICAL_OUTAGE                                                    │
│ Sentiment: HIGHLY_FRUSTRATED                                                │
│ Priority: P1_CRITICAL                                                       │
│ Action: Page On-Call                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
✨ Parsed Few-Shot Classification Results 
┌────────────────────┬───────────────────┐
│ Taxonomy Key       │ Assigned Value    │
├────────────────────┼───────────────────┤
│ Intent             │ TECHNICAL_OUTAGE  │
│ Sentiment          │ HIGHLY_FRUSTRATED │
│ Priority           │ P1_CRITICAL       │
│ Action             │ Page On-Call      │
└────────────────────┴───────────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/007-few-shot-prompting/main.py).

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/007-few-shot-prompting/main.py
```

---

## 🧪 Hands-On Experiments

1. **Test Order Sensitivity:** Rearrange the order of the few-shot examples. Does example ordering affect the model's prediction on borderline tickets?
2. **Negative Examples:** Add a negative example showing what NOT to do (e.g. `"Do NOT categorize pricing inquiries as TECHNICAL_OUTAGE"`).
