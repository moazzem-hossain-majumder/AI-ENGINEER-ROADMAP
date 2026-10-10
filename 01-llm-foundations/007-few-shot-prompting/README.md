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

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[System Persona] + [Few-Shot Demonstrations (Ex 1, 2, 3)] + [Unseen Test Query] ➔ [Consistent, Schema-Compliant Output]
```

1. **Zero-Shot Limitation:** If you ask an LLM to categorize a support ticket without examples, it often invents its own labels (e.g., `"Angry customer"`, `"Needs help"`, `"Payment issue"`), making downstream database ingestion impossible.
2. **In-Context Conditioning:** By providing 3 to 5 curated examples of exact inputs paired with the desired target outputs in the prompt:
   - The model's attention heads align with the exact taxonomy.
   - The output vocabulary and delimiter format are strictly adopted.
3. **Inference Execution:** When the unseen ambiguous test query arrives at the end of the prompt, the model completes the pattern naturally according to the established distribution.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, the system compares Zero-Shot vs. Few-Shot outputs on ambiguous tickets:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 007: FEW-SHOT PROMPTING    
===========================================================

🎫 Unseen Incoming Customer Ticket:
"We lost access to our production database after renewing our enterprise plan this morning. Fix this immediately!"

❌ Zero-Shot Classification (Unpredictable formatting & invented labels):
{
  "category": "Emergency Outage / Account issue",
  "mood": "Extremely mad",
  "urgency": "Highest"
}

✅ Few-Shot Classification (Strict taxonomy adhering to production schema):
┌────────────────────┬───────────────────────────────────────┐
│ Field              │ Classified Value                      │
├────────────────────┼───────────────────────────────────────┤
│ Intent             │ TECHNICAL_OUTAGE                      │
│ Sub-category       │ DATABASE_CONNECTIVITY                 │
│ Sentiment          │ HIGHLY_FRUSTRATED                     │
│ SLA Priority       │ P1_CRITICAL                           │
│ Action Required    │ Page On-Call Engineering Escalation   │
└────────────────────┴───────────────────────────────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/007-few-shot-prompting/main.py).

Key snippet:
```python
few_shot_prompt = f"""
Classify support tickets into:
Intent: [TECHNICAL_OUTAGE | BILLING_DISPUTE | FEATURE_REQUEST | ACCOUNT_ACCESS]
Priority: [P1_CRITICAL | P2_HIGH | P3_NORMAL]

Example 1:
Ticket: "I was double-billed on invoice #4928."
Output: Intent: BILLING_DISPUTE | Priority: P2_HIGH

Example 2:
Ticket: "Our entire team is locked out and getting 500 error."
Output: Intent: TECHNICAL_OUTAGE | Priority: P1_CRITICAL

Ticket: "{test_ticket}"
Output:
"""
```

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/007-few-shot-prompting/main.py
```

---

## 🧪 Hands-On Experiments

1. **Test Order Sensitivity:** Rearrange the order of the few-shot examples. Does example ordering affect the model's prediction on borderline tickets? *(Hint: LLMs often exhibit recency bias towards the final example).*
2. **Negative Examples:** Add a negative example showing what NOT to do (e.g. `"Do NOT categorize pricing inquiries as TECHNICAL_OUTAGE"`).
