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
- Before sampling each token, any token that would make the accumulated output invalid JSON syntax has its logit score forced to $-\infty$.
- This mathematically guarantees that the raw output is syntactically valid JSON.

---

## 🧩 Code Dissection: Why Did We Write It This Way?

For beginners reading [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/004-structured-outputs/main.py), here is why we used Pydantic V2 and JSON Mode instead of naive dictionary parsing:

### 1. `Pydantic` V2 Models vs. Raw Python Dictionaries (`json.loads`)
```python
class JobPosting(BaseModel):
    title: str
    min_years_experience: int
    required_skills: List[str]
    min_salary_usd: Optional[int]
```
* **Why did we write this?** Pydantic creates a **strict data contract**.
* **What could be written instead? (The Naive Way):**
  Using standard Python `json.loads`:
  ```python
  data = json.loads(raw_text)
  title = data.get("title")  # Could be None!
  exp = int(data.get("min_years_experience"))  # Crashes if model wrote "5 years" as a string!
  ```
* **Why Pydantic wins:**
  - **Type Coercion:** If the model outputs `"min_years_experience": "5"`, Pydantic automatically converts the string `"5"` into integer `5`.
  - **Fail-Fast Safety:** If mandatory fields are missing, Pydantic raises a descriptive `ValidationError` immediately, protecting your SQL database from corrupt data.
  - **IDE Autocomplete:** In your backend code, typing `job.` auto-suggests `.title`, `.company`, and `.required_skills` with full type safety.

---

### 2. `response_format={"type": "json_object"}` vs. Prompt-Only Begging
```python
response = client.chat.completions.create(
    ...,
    response_format={"type": "json_object"}
)
```
* **Why did we write this?** It forces the remote inference engine to constrain token sampling to valid JSON characters only.
* **What could be written instead?** Writing in the prompt: *"Please output only JSON, no markdown, no conversational words."*
* **Why prompt-only begging fails:** Models will occasionally ignore prompt instructions and output `Here is your JSON: ```json ...````. JSON Mode guarantees valid JSON syntax at the engine level.

---

### 3. Dynamic JSON Schema Generation via `model_json_schema()`
```python
schema_str = json.dumps(JobPosting.model_json_schema(), indent=2)
```
* **Why did we write this?** Instead of hand-writing prompt instructions describing the JSON keys, we let Pydantic generate the official JSON Schema automatically.
* **Why this wins:** If you update the Python class (e.g. adding a new field `is_remote_friendly: bool`), the system prompt updates automatically with zero chance of human typo errors.

---

### 4. Popular Alternatives in the Ecosystem
- **Instructor (`pip install instructor`):** A popular Python library that patches the OpenAI/Groq client to accept `response_model=JobPosting` directly.
- **Outlines (`pip install outlines`):** A research library for local models that compiles Pydantic schemas into finite state machines (FSMs) for guided decoding.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Declare the Data Contract (Pydantic Model):**
   Define typed attributes using `BaseModel` and `Field`.
2. **Step 2: Generate the JSON Schema for the Prompt:**
   Convert the model into JSON schema: `JobPosting.model_json_schema()`.
3. **Step 3: Construct the System Prompt:**
   Embed the schema string into instructions.
4. **Step 4: Execute API Call in JSON Mode:**
   Pass `response_format={"type": "json_object"}` at `temperature=0.0`.
5. **Step 5: Validate and Parse Output:**
   Call `JobPosting.model_validate_json(raw_text)`.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[1. Pydantic Model] ➔ [2. Export JSON Schema] ➔ [3. Inject into System Prompt] ➔ [4. LLM JSON Mode] ➔ [5. Pydantic Validation] ➔ [6. Clean Python Object]
```

1. **Schema Definition:** We define a standard Pydantic model (`JobPosting`) with precise typing.
2. **Schema Compilation:** We call `JobPosting.model_json_schema()` to get an industry-standard JSON Schema representation.
3. **JSON Mode Activation:** We pass `response_format={"type": "json_object"}`.
4. **Validation Guardrail:** We feed the raw output into `JobPosting.model_validate_json(raw_json)`.

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
