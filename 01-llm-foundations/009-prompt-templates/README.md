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

---

## 🧩 Code Dissection: Why Did We Write It This Way?

For beginners reading [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/009-prompt-templates/main.py), here is why we built a dedicated `PromptTemplate` engine:

### 1. Regex Introspection via `re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", template)`
```python
self.expected_vars = set(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", template))
```
* **Why did we write this?** To inspect the template text and discover all expected parameters dynamically at initialization.
* **Why regex?** It captures clean variable names matching standard Python identifiers (`[a-zA-Z_][a-zA-Z0-9_]*`), ignoring double brackets `{{...}}` used for escaping.

---

### 2. Set Difference Validation: `expected_vars - provided_vars`
```python
missing_vars = self.expected_vars - provided_vars
if missing_vars:
    raise ValueError(f"Missing required template variables: {missing_vars}")
```
* **Why did we write this?** To fail fast locally *before* making network requests.
* **The Business Impact:** If an upstream microservice fails to pass `company_name`, this code crashes locally in 0.001ms with a clear error message. Without this, your app sends a malformed prompt to the cloud, waits 2 seconds, pays $0.02 for the API call, and sends garbage to the user!

---

### 3. Functional Currying via `partial(**fixed_kwargs)`
```python
template.partial(sender_name="Moazzem", company="Synthetix AI")
```
* **Why did we write this?** In large organizations, some prompt parameters are constant (e.g. company signature, value proposition), while others are dynamic per customer.
* **How it works:** Pre-substitutes the static parameters and returns a lightweight new `PromptTemplate` instance that only expects the remaining dynamic variables.

---

### 4. Industry Alternatives: Jinja2 vs. LangChain
- **Jinja2:** A powerful templating language used by web frameworks (Django/Flask) and Hugging Face tokenizer chat templates. Excellent for complex conditionals (`{% if user.is_premium %}`).
- **LangChain `ChatPromptTemplate`:** Popular in framework-heavy stacks, but often introduces heavy third-party dependency bloat. Building a pure Python template engine provides identical functionality with zero external dependencies.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Parse Variables at Initialization:**
   Use regex to discover all `{variable}` placeholders.
2. **Step 2: Implement Defensive Formatting (`format`):**
   Compare expected vs provided keys using Python set difference.
3. **Step 3: Implement Message Construction (`format_messages`):**
   Return standard OpenAI/Groq messages format.
4. **Step 4: Implement Partial Binding (`partial`):**
   Substitute pre-filled keys and return a new instance.
5. **Step 5: Test Guardrails:**
   Verify that missing parameters raise a clear `ValueError`.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[Raw Template Text] ➔ [Regex Variable Extraction] ➔ [Validate Required Inputs] ➔ [Safe Interpolation] ➔ [Dispatch to LLM]
```

1. **Template Parsing:** Scans the text template to identify all required parameters.
2. **Defensive Validation:** Checks if any expected variables are missing.
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
