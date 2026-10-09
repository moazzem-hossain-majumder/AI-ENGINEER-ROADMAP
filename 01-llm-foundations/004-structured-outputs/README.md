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

## 📖 Concept Explanation: Unstructured Text vs. Typed Schemas

When you ask an LLM for data without constraints, it often responds with:
> *"Sure! Here is the data you requested: ```json { "name": ... } ``` Hope this helps!"*

If your backend code executes `json.loads(response)`, it crashes with a `JSONDecodeError` because of conversational preamble or markdown backticks!

```
Messy Natural Language ──➔ LLM with JSON Mode + Schema Prompt ──➔ Valid JSON String ──➔ Pydantic Validation ──➔ Strongly Typed Python Object
```

### The AI Engineer's Production Pattern
1. **Define Schema:** Create a Pydantic class specifying exact field names and types.
2. **Inject Schema:** Convert `Model.model_json_schema()` into the system prompt.
3. **Enforce JSON Mode:** Set `response_format={"type": "json_object"}`.
4. **Validate:** Pass the raw JSON string into `Model.model_validate_json(raw_text)`.

---

## 💻 What the Code Does (`main.py`)

In this project, we feed messy unstructured paragraph text about an AI job posting into the LLM:
> *"Looking for a Senior AI Engineer at Synthetix in San Francisco or Remote. Must have 4+ years of Python experience, deep knowledge of RAG architectures and PyTorch. Salary range is $180,000 to $220,000 with equity."*

The program parses this into a typed Pydantic class:
```python
class JobPosting(BaseModel):
    title: str
    company: str
    locations: List[str]
    min_years_experience: int
    required_skills: List[str]
    min_salary_usd: Optional[int]
    max_salary_usd: Optional[int]
```

And outputs a validated Python object ready to be inserted into a database.

---

## 🚀 How to Run

```bash
.\.venv\Scripts\python 01-llm-foundations/004-structured-outputs/main.py
```

---

## 🧪 Hands-On Experiments

1. **Add a Field:** Add `is_remote: bool` or `benefits: List[str]` to the `JobPosting` class in `main.py` and run it again.
2. **Test Validation Failure:** Intentionally provide an input that lacks numbers or has conflicting types to see how Pydantic protects your application.
