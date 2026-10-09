# 🟢 Project 002: Sampling Parameters & Determinism

> **Phase 01: LLM Foundations & Prompt Engineering**  
> *Master how Temperature, Top-P, and Max Tokens govern LLM creativity and reproducibility.*

---

## 🎯 Learning Outcomes
By completing this project, you will:
1. Understand how Large Language Models generate text one token at a time using probability distributions.
2. Master the **Temperature** parameter:
   - **`temperature = 0.0`** (Argmax / Greedy decoding): Strict determinism (best for classification, JSON parsing, code, math).
   - **`temperature = 0.7`** (Default balanced): Conversational natural fluency.
   - **`temperature = 1.4+`** (High entropy): Brainstorming, poetry, divergent creative ideas.
3. Master **`top_p`** (Nucleus Sampling): Dynamically truncating the tail of low-probability tokens.
4. Understand **`stop` sequences**: Halting generation immediately when a custom delimiter string is encountered.
5. Visually compare responses across multiple temperature settings side-by-side.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
Prompt ➔ Raw Model Logits ➔ Scale by Temperature (T) ➔ Softmax Probabilities ➔ Token Selection
```

1. **Greedy Argmax (T = 0.0):** At each step, the model identifies the token with the absolute highest probability score and picks it every time. When you run 3 calls in a row with $T=0.0$, the result is 100% deterministic and identical.
2. **Temperature Scaling (T > 0):** Dividing raw logits by $T$ flattens or sharpens the probability curve:
   - Low $T$ ($0.2$): Sharpens peaks; common tokens dominate.
   - High $T$ ($1.4$): Flattens differences; rare tokens are chosen more frequently, introducing novelty and surprise.
3. **Early Halting with Stop Sequences:** The model inference engine checks each emitted token against a blacklist array (`stop=["---"]`). The moment the string matches, token production is terminated instantly, avoiding unwanted generation.

---

## 📸 Sample Terminal Output & Run Walkthrough

When you execute `main.py`, here is the exact output displayed in your terminal:

```text
===========================================================
  AI ENGINEER ROADMAP - PROJECT 002: SAMPLING PARAMETERS   
===========================================================

1. Testing Determinism with Temperature = 0.0 (3 Identical Runs)
Greedy decoding always picks the token with highest probability (argmax).

Run #1 (T=0.0): An API (Application Programming Interface) is a set of rules 
and protocols that allows different software applications to communicate and 
exchange data with each other.
Run #2 (T=0.0): An API (Application Programming Interface) is a set of rules 
and protocols that allows different software applications to communicate and 
exchange data with each other.
Run #3 (T=0.0): An API (Application Programming Interface) is a set of rules 
and protocols that allows different software applications to communicate and 
exchange data with each other.

✔ Verified: All 3 outputs are 100% identical! Perfect for code, JSON & math.

2. Testing Temperature Spectrum on Creativity
    🎨 Temperature Comparison for: 'Name for an AI startup that    
                      optimizes GPU cooling.'                      
┌────────────────┬───────────────────────────┬────────────────────┐
│ Temperature    │ Sampling Behavior         │ Generated Response │
├────────────────┼───────────────────────────┼────────────────────┤
│ T = 0.0        │ Deterministic (Greedy)    │ ThermalEdge        │
│ T = 0.7        │ Balanced (Conversational) │ ThermalCore        │
│ T = 1.4        │ High Entropy              │ ThermZero          │
│                │ (Divergent/Creative)      │                    │
└────────────────┴───────────────────────────┴────────────────────┘

3. Testing Custom Stop Sequences (`stop=['---']`)
The model will stop producing tokens as soon as it writes '---'.

┌───────────────────── Without Stop Sequence (Full List) ─────────────────────┐
│ TensorFlow                                                                  │
│ PyTorch                                                                     │
│ Hugging Face Transformers                                                   │
│ ---                                                                         │
│ LangChain                                                                   │
│ Weights & Biases                                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌───────────────────── With stop=['---'] (Halted Early) ──────────────────────┐
│ TensorFlow                                                                  │
│ PyTorch                                                                     │
│ Hugging Face Transformers                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Reference

The complete runnable code is located in [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/002-sampling-parameters/main.py).

---

## 🚀 How to Run and Check

Run this single command from your terminal:

```powershell
.\.venv\Scripts\python 01-llm-foundations/002-sampling-parameters/main.py
```

---

## 🧪 Hands-On Experiments

1. **Verify Determinism:** Run `main.py` multiple times in a row. Confirm that `Run #1`, `Run #2`, and `Run #3` never change a single character.
2. **Push High Temperature:** In [`main.py`](file:///d:/AI%20ENGINEER%20ROADMAP/AI-ENGINEER-ROADMAP/01-llm-foundations/002-sampling-parameters/main.py), change `1.4` to `1.8` or `2.0`. Notice at what point words turn into surreal associations.
3. **Multi-Stop Sequences:** Pass multiple stop delimiters like `stop=["\n", "###"]` to truncate at the first newline.
