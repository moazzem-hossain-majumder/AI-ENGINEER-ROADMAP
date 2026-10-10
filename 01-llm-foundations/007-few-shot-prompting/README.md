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

---

## 🧩 Code Dissection: Why Did We Write It This Way?

For beginners reading [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/007-few-shot-prompting/main.py), here is why few-shot prompting is structured this way:

### 1. Few-Shot In-Context Learning vs. Traditional BERT Fine-Tuning
```python
few_shot_prompt = """
Example 1:
Ticket: "I was charged twice..."
Intent: BILLING_DISPUTE
...
"""
```
* **Why did we write this?** To achieve production-grade domain classification in **5 minutes** without machine learning training infrastructure.
* **What could be written instead? (The Traditional ML Alternative):**
  Training a traditional classifier (e.g. fine-tuning BERT, RoBERTa, or Scikit-learn Logistic Regression).
* **Trade-offs:**
  - *Traditional BERT:* Requires collecting 2,000 manually labeled tickets, writing PyTorch training scripts, managing GPU clusters, and hosting a custom model container.
  - *Few-Shot LLM:* Requires only 3 canonical examples written by a domain expert. It adapts instantly to new business categories without re-training models.

---

### 2. Separating Examples with Explicit Delimiters (`---`)
* **Why use delimiters between examples?**
  Transformers are pattern-completion machines. If examples bleed into each other without clear delimiters like `---`, the model can treat Example 2 as continuation of Example 1, leading to degraded predictions.

---

### 3. Parsing with `line.split(":", 1)`
```python
for line in few_shot_res.split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
```
* **Why `split(":", 1)`?**
  Passing `1` limits the split to the *first* colon encountered. If the generated text contains a timestamp (e.g. `Action: Call customer at 10:30 AM`), naive `split(":")` would break the value into multiple fragments.

---

### 4. Advanced Ecosystem Alternative: DSPy
In modern production pipelines, instead of hand-tuning few-shot examples, engineers use **DSPy** (Stanford NLP):
- DSPy compiles prompts algorithmically, testing hundreds of combinations of few-shot examples and picking the set that maximizes classification accuracy against a validation dataset.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Define the Closed Taxonomy:**
   Decide the exact enumerated values your enterprise software expects.
2. **Step 2: Construct Balanced Canonical Examples:**
   Write 3 to 4 distinct examples covering different classes.
3. **Step 3: Build the Prompt Assembler:**
   Append the unseen test ticket to the bottom of the prompt and leave the output field open for completion.
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
