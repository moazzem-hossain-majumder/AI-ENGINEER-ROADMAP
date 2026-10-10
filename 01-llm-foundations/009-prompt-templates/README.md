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

## 📚 Background Knowledge & Theory (Read Before Coding)

To build maintainable, modular AI applications, you must understand prompt architecture patterns.

### 1. The Anti-Pattern of Hardcoded F-Strings
In toy tutorials, developers often write:
```python
prompt = f"Write an email to {prospect_name} at {company}."
```
In real production systems, this creates severe engineering headaches:
1. **Silent Failures:** If `prospect_name` is `None` or omitted, Python silently renders `"Write an email to None at Microsoft"`, wasting API tokens and sending embarrassing messages to customers.
2. **Escaping Collisions:** If your prompt contains JSON examples with `{ "key": "value" }`, Python f-strings throw syntax errors unless every bracket is manually doubled to `{{ "key": "value" }}`.
3. **No Introspection:** Backend services cannot automatically query a prompt to ask: *"What parameters do you require before I can render you?"*
4. **Poor Separation of Concerns:** Non-technical domain experts or prompt engineers cannot update prompts stored inside hardcoded Python functions without touching application logic.

### 2. The Solution: Declarative Prompt Templates
A production `PromptTemplate` engine separates the **template structure** from the **runtime arguments**:
- **Automatic Introspection:** Scans the template string at initialization using regular expressions to extract the exact list of required variables:
  
  $$\text{Expected Vars} = \text{RegexScan}(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}") $$

- **Pre-Flight Validation:** Compares the expected variables with the supplied keyword arguments using set theory:
  
  $$\text{Missing} = \text{Expected} \setminus \text{Provided}$$
  
  If $\text{Missing} \neq \emptyset$, it raises an immediate exception *before* dispatching network calls.

### 3. Functional Currying (Partial Parameter Binding)
Often, some parameters are fixed across an entire tenant or workflow (e.g. sender name, company value proposition), while others vary per user (e.g. prospect name, recent milestone).
**Partial formatting** allows you to pre-bind a subset of variables, returning a new `PromptTemplate` ready to receive the remaining dynamic variables later in the pipeline.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Parse Variables at Initialization:**
   ```python
   import re

   class PromptTemplate:
       def __init__(self, template: str, system_prompt: str = ""):
           self.template = template
           self.system_prompt = system_prompt
           self.expected_vars = set(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", template))
   ```
2. **Step 2: Implement Defensive Formatting (`format`):**
   ```python
   def format(self, **kwargs) -> str:
       provided_vars = set(kwargs.keys())
       missing = self.expected_vars - provided_vars
       if missing:
           raise ValueError(f"Missing required variables: {missing}")
       return self.template.format(**kwargs)
   ```
3. **Step 3: Implement Message Construction (`format_messages`):**
   Return standard OpenAI/Groq messages format `[{"role": "system", ...}, {"role": "user", ...}]`.
4. **Step 4: Implement Partial Binding (`partial`):**
   Create a copy of the template where specified keys are substituted immediately, leaving remaining placeholders intact.
5. **Step 5: Test Guardrails:**
   Demonstrate that omitting a required variable raises a clear error rather than sending broken prompts to the API.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[Raw Template Text] ➔ [Regex Variable Extraction] ➔ [Validate Required Inputs] ➔ [Safe Interpolation] ➔ [Dispatch to LLM]
```

1. **Template Parsing:** The `PromptTemplate` class scans the text template using regex to identify all required parameters.
2. **Defensive Validation:** Before running inference, checks if any expected variables are missing.
3. **Partial Binding:** Pre-binds fixed parameters and allows dynamic parameters to be supplied later.
4. **LLM Generation:** Dispatches the cleanly composed prompt to generate tailored output.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, you will see template variable inspection, validation, and generation:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 009: PROMPT TEMPLATES      
===========================================================

   📋 Template Variable Contract   
┌──────────────────────┬──────────┐
│ Placeholder Variable │ Status   │
├──────────────────────┼──────────┤
│ {pain_point}         │ Required │
│ {prospect_company}   │ Required │
│ {prospect_name}      │ Required │
│ {recent_milestone}   │ Required │
│ {solution_value}     │ Required │
└──────────────────────┴──────────┘

🛡️ Running Defensive Validation Test (Missing Parameter)...
┌─────────────────────── ✔ Validation Guardrail Active ───────────────────────┐
│ Caught Expected Error: Missing required template variables:                 │
│ ['recent_milestone']. Provided: ['pain_point', 'prospect_company',          │
│ 'prospect_name', 'solution_value']                                          │
└─────────────────────────────────────────────────────────────────────────────┘
┌───────────────── 🚀 Rendered User Prompt Dispatched to LLM ─────────────────┐
│ Write a compelling, concise enterprise partnership email to Satya, who is   │
│ leading infrastructure at Microsoft.                                        │
│                                                                             │
│ Reference their recent milestone: 'Expansion of Azure hyperscale data       │
│ centers'.                                                                   │
│ Address their core pain point: 'Inference memory bottlenecks and rising     │
│ power consumption'.                                                         │
│ Position our solution: 'Synthetix AI's dynamic KV-cache compression engine  │
│ (40% RAM savings)'.                                                         │
│ Call to action: Ask for a short 10-minute briefing next week.               │
│ Keep the tone direct, technical, and respectful of an executive's time.     │
└─────────────────────────────────────────────────────────────────────────────┘
┌───────────────── 📧 Generated Personalized Executive Email ─────────────────┐
│ Subject: 40% RAM reduction for Azure inference workloads                    │
│                                                                             │
│ Hi Satya,                                                                   │
│                                                                             │
│ Congrats on the Azure hyperscale expansion. While scale solves compute, it  │
│ doesn’t solve the physics of inference.                                     │
│                                                                             │
│ Currently, KV-cache memory bottlenecks are driving up both latency and      │
│ power consumption across large-scale LLM deployments. We built Synthetix    │
│ AI’s dynamic KV-cache compression engine to address this directly.          │
│                                                                             │
│ In production benchmarks, we deliver a 40% reduction in RAM usage without   │
│ degrading token quality or increasing compute overhead.                     │
│                                                                             │
│ I know your calendar is tight. Are you open to a 10-minute technical        │
│ briefing next week to review the data?                                      │
│                                                                             │
│ Best,                                                                       │
│ Moazzem Hossain Majumder                                                    │
│ Synthetix AI                                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/009-prompt-templates/main.py).

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
