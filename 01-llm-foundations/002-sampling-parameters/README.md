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

## 📚 Background Knowledge & Theory (Read Before Coding)

To master LLM generation and build sampling experiments from scratch, you need to understand how the transformer's final layer produces text.

### 1. From Raw Logits to Probabilities
Inside the transformer, the final linear layer outputs a vector of raw, unnormalized scores called **Logits ($z$)**—one real number for each of the ~100,000 words in its vocabulary.

To convert these raw scores into valid probabilities that sum to 1.0 (100%), the model applies the **Softmax function**:

$$P(token_i) = \frac{e^{z_i}}{\sum_{j} e^{z_j}}$$

### 2. The Mathematics of Temperature ($T$)
Temperature is a scaling factor injected into the Softmax exponent:

$$P(token_i) = \frac{e^{z_i / T}}{\sum_{j} e^{z_j / T}}$$

```
[Raw Logits: z] ──➔ [Divide by Temperature: z / T] ──➔ [Exponentiate & Normalize: Softmax] ──➔ [Next Token Probability]
```

- **When $T \to 0$ (Greedy / Argmax Decoding):**
  Dividing logits by a tiny fraction magnifies small differences. The highest-scoring token skyrockets towards $1.0$ probability, while all other tokens drop to $0.0$. The model **always picks the highest-ranking token**, making outputs 100% deterministic and reproducible across multiple runs.
  *Use Case:* SQL queries, JSON generation, math, and unit tests.

- **When $T = 0.7$ (Balanced):**
  Normal conversational range. High-probability tokens are favored, but minor variations are allowed, making dialogue sound natural and human.

- **When $T > 1.2$ (High Entropy):**
  Dividing logits by a large number flattens the curve. The difference between common tokens and rare tokens diminishes. Low-probability, unusual words have a much higher chance of being selected, boosting divergent creativity—or inducing hallucinations if pushed above $1.8$.

### 3. Nucleus Sampling (`top_p`)
Introduced by Holtzman et al. (2019), **Nucleus Sampling** solves the problem of "sampling from the long tail" of ridiculous tokens.
Instead of setting a fixed cutoff (like Top-K which picks the top $K$ tokens), `top_p = 0.9` dynamically sorts tokens by probability and keeps only the smallest subset whose cumulative probability reaches 90%. If the top token already has 95% probability, only that token is considered!

### 4. Stopping Criteria (`stop` sequences)
During autoregressive generation, the model terminates when:
1. It predicts the internal `<|end_of_text|>` or `<|eot_id|>` token.
2. It hits the client-specified `max_tokens` limit.
3. It emits a user-defined string listed in `stop=["---", "\n\n"]`.

---

## 🏗️ Step-by-Step Blueprint: How to Code This from Scratch

1. **Step 1: Verify Determinism:**
   - Loop 3 times over the exact same prompt with `temperature=0.0`.
   - Store results in a list: `outputs.append(response.choices[0].message.content)`.
   - Assert `len(set(outputs)) == 1` to verify every character is identical.
2. **Step 2: Compare Creativity Spectrum:**
   - Iterate over a list of temperatures `[0.0, 0.7, 1.4]`.
   - Send the same creative prompt (e.g. startup naming).
   - Render a comparison table showing how outputs vary from conservative to wild.
3. **Step 3: Implement Stop Sequences:**
   - Prompt the model to write a numbered list.
   - Run once without `stop`, and once with `stop=["---"]`.
   - Verify that generation halts early, saving tokens and cutting off unwanted content.

---

## ⚙️ How It Works (Step-by-Step Execution Flow)

```
Prompt ➔ Raw Model Logits ➔ Scale by Temperature (T) ➔ Softmax Probabilities ➔ Token Selection
```

1. **Greedy Argmax (T = 0.0):** Picks the highest probability token at every step.
2. **Temperature Scaling (T > 0):** Dividing raw logits by $T$ flattens or sharpens the distribution.
3. **Early Halting with Stop Sequences:** The inference engine checks each emitted token against a blacklist array (`stop=["---"]`) and halts production immediately.

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
