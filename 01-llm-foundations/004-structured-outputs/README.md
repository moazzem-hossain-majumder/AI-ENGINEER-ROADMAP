# 🟢 Project 004: Structured Outputs & Schema Validation

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Transform unpredictable, messy natural language into strongly-typed, schema-validated JSON data with Pydantic.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand why unstructured text output from LLMs breaks downstream production software.
2. Enable JSON Mode via `response_format={"type": "json_object"}`.
3. Define strict data contracts using **Pydantic V2** (`BaseModel`, `Field`, typed collections).
4. Parse and validate LLM outputs directly into typed Python objects.
5. Implement defensive fallback handling for malformed JSON or schema mismatches.

---

## 📚 Background Knowledge & Theory (Read Before Coding)

To build reliable data pipelines with LLMs, you must understand constrained generation and type validation.

### 1. The Natural Language Dilemma in Production Software
Modern LLMs are aligned with Reinforcement Learning from Human Feedback (RLHF) to behave like conversational assistants. When asked for data, a model naturally wants to be polite:
> *"Here is the information you requested: ```json { "title": ... } ``` Let me know if you need anything else!"*

If downstream backend code feeds this response directly into Python's `json.loads()`, the program crashes with a fatal `json.decoder.JSONDecodeError` because of conversational preamble, trailing markdown backticks, or unescaped characters.

### 2. How JSON Mode Works Under the Hood (Grammar-Guided Decoding)
When you enable `response_format={"type": "json_object"}`, the inference engine does something profound at the tokenizer level:
- It activates a **Context-Free Grammar (CFG)** parser during token generation.
- Before sampling each token, any token that would make the accumulated output invalid JSON syntax (such as two consecutive commas `,,` or a missing closing quote) has its logit score forced to $-\infty$.
- This mathematically guarantees that the raw output is syntactically valid JSON.

### 3. Syntax vs. Schema: Why JSON Mode Alone Is Not Enough
JSON Mode guarantees valid **JSON syntax** (curly braces and quotes), but it does **not** guarantee your **business schema**:
- The model might return `{"job_name": ...}` instead of `{"title": ...}`.
- It might return a string `"five"` where your SQL database requires an integer `5`.
- A mandatory field might be omitted entirely.

This is why production AI systems combine **JSON Mode** with **Pydantic V2**:
- **JSON Mode** ensures valid JSON syntax.
- **Pydantic** enforces type safety, default values, mandatory fields, and data validation rules at C-speed via `pydantic-core`.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Declare the Data Contract (Pydantic Model):**
   ```python
   from pydantic import BaseModel, Field
   from typing import List, Optional

   class JobPosting(BaseModel):
       title: str = Field(description="Exact job title")
       company: str = Field(description="Hiring company")
       min_years_experience: int = Field(description="Minimum years required")
       required_skills: List[str] = Field(description="Skills list")
       is_remote_friendly: bool
   ```
2. **Step 2: Generate the JSON Schema for the Prompt:**
   Convert the model into an industry-standard JSON schema:
   `schema_str = json.dumps(JobPosting.model_json_schema(), indent=2)`
3. **Step 3: Construct the System Prompt:**
   Instruct the model: *"You are an extraction engine. Output raw JSON conforming to this schema only. Do not output markdown backticks."*
4. **Step 4: Execute API Call in JSON Mode:**
   Call `client.chat.completions.create(..., response_format={"type": "json_object"}, temperature=0.0)`.
5. **Step 5: Validate and Parse Output:**
   Pass the text into `JobPosting.model_validate_json(raw_response)`. Catch `pydantic.ValidationError` to defend against invalid fields.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[1. Pydantic Model] ➔ [2. Export JSON Schema] ➔ [3. Inject into System Prompt] ➔ [4. LLM JSON Mode] ➔ [5. Pydantic Validation] ➔ [6. Clean Python Object]
```

1. **Schema Definition:** We define a standard Pydantic model (`JobPosting`) with precise typing (`int`, `bool`, `List[str]`).
2. **Schema Compilation:** We call `JobPosting.model_json_schema()` to get an industry-standard JSON Schema representation and embed it directly into the LLM system prompt.
3. **JSON Mode Activation:** We pass `response_format={"type": "json_object"}` in the API call.
4. **Validation Guardrail:** We feed the raw output into `JobPosting.model_validate_json(raw_json)`. If any key is missing or of the wrong type, Pydantic catches it immediately.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, here is the exact visual walkthrough of the extraction process:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 004: STRUCTURED OUTPUTS    
===========================================================

┌───────────────── 📄 Raw Unstructured Job Description Input ─────────────────┐
│ Synthetix AI is searching for a Lead Machine Learning Engineer! Our         │
│ headquarters are based in San Francisco, CA, but this role can be 100%      │
│ remote anywhere in the US. Applicants should have at least 5 years of       │
│ production coding experience with Python. Key qualifications include deep   │
│ expertise with PyTorch, Vector Databases like Chroma or Pinecone, and       │
│ experience deploying RAG pipelines. We offer a competitive base             │
│ compensation of $190,000 to $240,000 plus substantial equity and full       │
│ medical benefits.                                                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────── 🔍 Raw JSON Returned by LLM (JSON Mode) ──────────────────┐
│ {                                                                           │
│   "title": "Lead Machine Learning Engineer",                                │
│   "company": "Synthetix AI",                                                │
│   "locations": [                                                            │
│     "San Francisco, CA",                                                    │
│     "Remote (US)"                                                           │
│   ],                                                                        │
│   "is_remote_friendly": true,                                               │
│   "min_years_experience": 5,                                                │
│   "required_skills": [                                                      │
│     "Python",                                                               │
│     "PyTorch",                                                              │
│     "Vector Databases (Chroma, Pinecone)",                                  │
│     "RAG pipelines"                                                         │
│   ],                                                                        │
│   "min_salary_usd": 190000,                                                 │
│   "max_salary_usd": 240000                                                  │
│ }                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘

                    ✨ Validated Pydantic JobPosting Object                    
┌────────────────────────┬────────────────────────────────────────────────────┐
│ Field                  │ Validated Value                                    │
├────────────────────────┼────────────────────────────────────────────────────┤
│ Title                  │ Lead Machine Learning Engineer                     │
│ Company                │ Synthetix AI                                       │
│ Locations              │ San Francisco, CA, Remote (US)                     │
│ Remote Friendly        │ ✅ Yes                                             │
│ Min Experience         │ 5 years                                            │
│ Required Skills        │ Python, PyTorch, Vector Databases (Chroma,         │
│                        │ Pinecone), RAG pipelines                           │
│ Salary Range (USD)     │ $190,000 - $240,000                                │
└────────────────────────┴────────────────────────────────────────────────────┘

✔ Success: Object is now a strongly typed Python instance ready for database 
storage!
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/004-structured-outputs/main.py).

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/004-structured-outputs/main.py
```

---

## 🧪 Hands-On Experiments

1. **Add Custom Fields:** In [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/004-structured-outputs/main.py), add `benefits: List[str]` or `is_senior: bool` to the `JobPosting` class and re-run.
2. **Test With Different Text:** Replace `messy_text` with an unstructured job listing from LinkedIn or an invoice paragraph. Notice how reliably the data schema is populated.
