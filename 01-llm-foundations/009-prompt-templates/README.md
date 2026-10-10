# 🟢 Project 009: Prompt Templates & Dynamic Interpolation

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Build modular, validated, production-grade prompt templates with missing-variable guardrails and partial interpolation.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand why hardcoded `f"..."` strings fail in production codebases (untyped, hard to version, unvalidated).
2. Build a standalone `PromptTemplate` class that inspects and validates `{variable}` parameters.
3. Prevent runtime production bugs by asserting that all required schema variables exist before making API calls.
4. Support **partial formatting** (currying templates with shared baseline parameters).
5. Build an automated Personalized Enterprise Partnership Email Generator.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[Raw Template Text] ➔ [Regex Variable Extraction] ➔ [Validate Required Inputs] ➔ [Safe Interpolation] ➔ [Dispatch to LLM]
```

1. **Template Parsing:** The `PromptTemplate` class scans the text template using regex `r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}"` to identify all required parameters (e.g., `{company_name}`, `{pain_point}`).
2. **Defensive Validation:** Before running inference, the `format(**kwargs)` method checks:
   - Are any expected variables missing? If yes, raises a `ValueError` immediately *before* spending tokens or making a network call.
3. **Partial Binding:** You can pre-bind fixed parameters (such as sender signature or product description) and allow dynamic parameters (such as prospect name or news) to be supplied later.
4. **LLM Generation:** The cleanly composed prompt is dispatched to generate tailored, personalized output.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, you will see template variable inspection, validation, and generation:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 009: PROMPT TEMPLATES      
===========================================================

📋 Template Variable Contract:
Required Parameters: ['prospect_name', 'prospect_company', 'recent_milestone', 'pain_point', 'solution_value']

🛡️ Validation Defense Check:
Attempting to format template with missing parameter 'recent_milestone'...
[Caught Expected Error] Missing required template variables: {'recent_milestone'}

✨ Fully Populated Prompt Sent to LLM:
--------------------------------------------------
Prospect: Satya | Company: Microsoft
Milestone: Opening of new Atlanta AI Data Center
Pain Point: High GPU cooling costs and inference latency bottlenecks
Solution: Synthetix AI's dynamic KV-cache compression technology
--------------------------------------------------

📧 Generated Personalized Executive Outreach:
Subject: Scaling Atlanta's AI throughput: 40% reduction in KV-cache memory

Hi Satya,

Congratulations on the recent launch of Microsoft's new Atlanta AI Data Center—
a massive milestone for hyperscale infrastructure.

As your clusters scale to meet unprecedented demand, managing inference memory
bottlenecks and GPU cooling costs becomes paramount. Synthetix AI's dynamic
KV-cache compression technology delivers a 40% reduction in memory footprint
without degradation in model accuracy.

Would you or your infrastructure team be open to a 10-minute briefing next week
to see our benchmarking data on Blackwell and Hopper clusters?

Best regards,
Moazzem Hossain Majumder
Lead AI Architect, Synthetix AI
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/009-prompt-templates/main.py).

Key snippet:
```python
template = PromptTemplate(
    template="Write an email to {prospect_name} at {company} regarding {product}.",
    system_role="You are an enterprise sales director."
)

# Throws error if variables are missing
formatted_messages = template.format_messages(
    prospect_name="Satya",
    company="Microsoft",
    product="KV-Cache Optimization"
)
```

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/009-prompt-templates/main.py
```

---

## 🧪 Hands-On Experiments

1. **Add Custom Parameters:** Add `{sender_title}` and `{meeting_duration}` to the template in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/009-prompt-templates/main.py) and test the output.
2. **Template Composition:** Create two templates (one for the email subject line and one for the email body) and chain them together.
