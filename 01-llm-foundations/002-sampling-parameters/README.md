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

## 📖 Concept Explanation: What happens inside the model?

At every single step, an LLM outputs raw scores called **logits** for every token in its vocabulary (~100,000 tokens).

These logits pass through a **Softmax function** modified by **Temperature ($T$)**:

$$P(token_i) = \frac{e^{z_i / T}}{\sum_{j} e^{z_j / T}}$$

```
Logits (raw scores) ──➔ Divide by Temperature (T) ──➔ Softmax ──➔ Next Token Probability
```

* **When $T \to 0$:** The highest scoring token dominates with near 100% probability. The model always picks the exact same token (Greedy Decoding).
* **When $T = 1.0$:** The model samples directly from the raw trained probability distribution.
* **When $T > 1.0$:** The probabilities flatten out. Rare and unexpected tokens have a much higher chance of being chosen, increasing randomness and creativity.

### Nucleus Sampling (`top_p`)
Instead of considering all 100,000 tokens, `top_p = 0.9` tells the model: *only consider the smallest set of top tokens whose cumulative probability adds up to 90%. Discard the bottom 10% completely.*

---

## 💻 What the Code Does (`main.py`)

1. Sends the **exact same prompt** 3 times at `temperature = 0.0`.
   - *Observation:* The outputs are 100% identical every single time!
2. Sends the prompt at `temperature = 0.7`.
   - *Observation:* Natural, fluent response.
3. Sends the prompt at `temperature = 1.4`.
   - *Observation:* Wild, creative, colorful variations.
4. Demonstrates a custom **`stop` sequence** (e.g., stopping generation at `"\n\n"` or `"---"`).

---

## 🚀 How to Run

```bash
.\.venv\Scripts\python 01-llm-foundations/002-sampling-parameters/main.py
```

---

## 🧪 Hands-On Experiments

1. **Verify Determinism:** Run `main.py` multiple times. Does `temp = 0.0` ever change?
2. **Push the limits:** Change the high temperature to `1.8` or `2.0`. Notice at what point the text degenerates into nonsense (hallucinations/gibberish).
3. **Use Stop Sequences:** Set `stop=["###"]` and observe how the model ceases output generation immediately upon outputting that marker.
