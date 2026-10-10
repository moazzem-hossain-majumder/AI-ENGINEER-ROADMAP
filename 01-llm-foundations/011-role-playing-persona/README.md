# 🟢 Project 011: Dynamic System Personas & Tone Control

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Control vocabulary distribution, audience adaptation, and behavioral guardrails via dynamic persona conditioning.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand how system prompts steer the underlying token probability distribution toward specific lexical domains.
2. Master persona conditioning: vocabulary constraints, stylistic register, assumed audience expertise, and length limits.
3. Build a dynamic multi-persona engine that explains the exact same complex AI concept across three audiences:
   - **ELI5 (5-Year-Old):** Friendly analogies, zero jargon.
   - **Principal Systems Engineer:** High-dimensional vector math, algorithmic indexing, hardware caching.
   - **Enterprise Legal Counsel:** Data governance, IP risks, PII compliance, and copyright liability.
4. Analyze lexical differences and tone metrics across persona outputs.

---

## 📚 Background Knowledge & Theory (Read Before Coding)

To build adaptive AI assistants that communicate effectively with diverse end-users, you must understand behavioral conditioning in transformer decoders.

### 1. The Mechanics of Persona Conditioning
During training, a foundational LLM ingests trillions of tokens from diverse sources: children's stories, academic papers, Reddit posts, and legal briefs.
- The model contains representations of all these distinct linguistic registers.
- Without a system prompt, the model defaults to a generic, corporate assistant persona ("RLHF default mode").
- The **system prompt acts as a prior probability filter**: it elevates the likelihood of vocabulary associated with the specified persona while suppressing terms outside of it.

```
[Raw Model Vocabulary: ~100k Tokens]
                 │
                 ├── System: "You are talking to a 5-year-old" ──➔ Elevates: ["library", "coloring", "toy", "friendly"]
                 │                                                Suppresses: ["hyperplane", "stochastic", "eigenvector"]
                 │
                 └── System: "You are a Principal Engineer"  ──➔ Elevates: ["cosine distance", "ANN indexing", "latency"]
                                                                  Suppresses: ["magic", "super fun", "kiddos"]
```

### 2. The 4 Pillars of a Production Persona Contract
A production persona system prompt must define four explicit constraints:
1. **Target Audience Profile:** What is their existing knowledge level? (e.g., *"Assume reader has zero CS knowledge"* vs *"Assume reader has a PhD in Math"*).
2. **Vocabulary Guardrails:** Whitelisted analogies and blacklisted jargon terms.
3. **Tone & Register:** Enthusiastic, strictly objective, cynical, or conservative.
4. **Output Format & Length:** Bullet points vs prose, 2 sentences vs 3 paragraphs.

### 3. Persona Drift in Long Conversations
In multi-turn chats, models often suffer from **Persona Drift**:
- As user turns accumulate, the model begins mirroring the user's conversational tone rather than strictly adhering to its initial persona.
- *Production Solution:* Re-affirm key persona constraints in periodic system prompt reminders or keep the pinned system prompt explicit and concise.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Define Persona Specifications:**
   Create a dataclass or dictionary defining each persona's name, description, and detailed system prompt:
   ```python
   @dataclass
   class Persona:
       name: str
       target_audience: str
       system_prompt: str
   ```
2. **Step 2: Craft the Target Personas:**
   - Persona A: Kindergarten Teacher (simple metaphors).
   - Persona B: Staff Infrastructure Engineer (rigorous systems architecture).
   - Persona C: Corporate General Counsel (regulatory compliance & risk).
3. **Step 3: Dispatch Prompt Across Personas:**
   Feed the identical technical question (e.g., *"What is a vector embedding and how does it work?"*) to all three personas using `temperature=0.7`.
4. **Step 4: Compare & Measure Outputs:**
   Display the generated responses side-by-side in styled panels and analyze the vocabulary differences.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
[Technical Subject Query] ➔ [Iterate Personas] ➔ [Apply Role Constraints] ➔ [Generate Tailored Explanations] ➔ [Display Comparative Analysis]
```

1. **Query Selection:** A challenging technical topic is chosen (*Vector Embeddings*).
2. **System Prompt Injection:** For each persona, the system prompt conditions the model's vocabulary and role before the user prompt is processed.
3. **Generation:** The model responds, strictly constrained by the persona's designated perspective.
4. **Evaluation:** Responses are presented side-by-side to demonstrate the versatility of persona conditioning.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, you will see how the same technical concept is adapted across audiences:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 011: ROLE-PLAYING PERSONA  
===========================================================

📌 Technical Topic: "What is a Vector Embedding and why do we use it in AI?"

┌────────── 🧸 Persona 1: ELI5 (Explain Like I'm 5 / Kindergarten) ──────────┐
│ Imagine you have a giant toy chest! Instead of tossing toys in a messy pile,│
│ you put all the animal toys on one shelf, all the race cars on another, and │
│ all the puzzle games in a basket.                                           │
│                                                                             │
│ A vector embedding is like giving every toy a secret map address so that    │
│ toys that are best friends are always sitting right next to each other!     │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────── 💻 Persona 2: Principal Distributed Systems Engineer ───────────────┐
│ A vector embedding is a continuous, dense mathematical mapping from a       │
│ discrete token space into a d-dimensional Euclidean metric space (e.g.,     │
│ d=1536).                                                                    │
│                                                                             │
│ We use them because linear algebra operations—specifically cosine distance  │
│ or dot products—allow sub-linear Approximate Nearest Neighbor (ANN) search  │
│ via HNSW graphs, enabling semantic retrieval across millions of documents in│
│ under 15ms.                                                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌───────────── ⚖️ Persona 3: Enterprise Legal & Compliance Counsel ───────────┐
│ Vector embeddings represent mathematical derivatives of proprietary input   │
│ source texts.                                                               │
│                                                                             │
│ From a compliance perspective, embeddings mitigate direct copyright exposure│
│ because they store latent vector weights rather than verbatim source text,  │
│ but require strict data governance to ensure sensitive PII cannot be        │
│ reconstructed through inversion attacks.                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/011-role-playing-persona/main.py).

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/011-role-playing-persona/main.py
```

---

## 🧪 Hands-On Experiments

1. **Add an Angry Tech Support Persona:** Create a persona that acts like an overworked, cynical sysadmin answering user queries.
2. **Shakespearean Translator:** Create a persona that answers modern software engineering questions in Elizabethan iambic pentameter.
