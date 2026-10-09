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

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[1. Pydantic Model] ➔ [2. Export JSON Schema] ➔ [3. Inject into System Prompt] ➔ [4. LLM JSON Mode] ➔ [5. Pydantic Validation] ➔ [6. Clean Python Object]
```

1. **Schema Definition:** We define a standard Pydantic model (`JobPosting`) with precise typing (`int`, `bool`, `List[str]`).
2. **Schema Compilation:** We call `JobPosting.model_json_schema()` to get an industry-standard JSON Schema representation and embed it directly into the LLM system prompt.
3. **JSON Mode Activation:** We pass `response_format={"type": "json_object"}` in the API call. This forces the model engine's tokenizer to emit valid JSON tokens only.
4. **Validation Guardrail:** We feed the raw output into `JobPosting.model_validate_json(raw_json)`. If any key is missing or of the wrong type (e.g. string instead of int), Pydantic catches it immediately before corrupting your database.

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
