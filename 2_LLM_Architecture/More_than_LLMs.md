## 1. Efficient LLMs at Inference Time

### Agenda
* Efficient LLMs at Inference Time
* New LLM Architectures
* Deployment Trends: SLMs & Parallelism
* Summary Table: Optimization Tradeoffs


Serving an LLM is not a uniform task; today's engineering focuses on how to serve models to millions of users without massive latency or cost.

### The Inference Bottleneck: Two Distinct Phases
In auto-regressive models, inference is split into two phases with fundamentally different hardware requirements:

* **Pre-fill (Compute-Intensive)**: Processes the entire user prompt as a large matrix to understand context and initialize the KV cache. It determines the **Time to First Token (TTFT)**.
* **Decode (Memory-Intensive)**: Generates the output token-by-token sequentially. It cannot be parallelized and is limited by GPU memory bandwidth, determining the **Time Per Output Token (TPOT)**.



### Caching: The History Database
To avoid re-reading the entire conversation for every new word, models use caching.
* **KV Cache**: Stores the "Key" and "Value" vectors for past tokens.
* **Prefix Caching**: Caches repetitive prompt parts (like system instructions) across multiple users or sessions to speed up responses.

> [!TIP]
> **The Query Vector ($Q$)**: The $Q$ vector is not cached because it is only needed for the current token's attention calculation; discarding it saves ~33% of GPU memory.

---

## 2. New LLM Architectures
Modern models use specific "pivots" on the original Transformer architecture to handle longer sequences and specialized tasks.

### RoPE (Rotary Positional Embedding)
Instead of adding absolute coordinate vectors, RoPE rotates the $Q$ and $K$ vectors.
* **Relative Distance**: Attention scores depend purely on the difference between token angles ($\cos((m - n)\theta)$), meaning the model only "sees" how far apart words are.
* **Extrapolation**: Allows models to handle massive context windows and generalize to longer sequences than seen in training.

### MoE (Mixture of Experts)
A technique that uses a subset of specialized "experts" to improve quality without increasing compute cost per token.
* **Router**: A learned gate network that scores experts and selects the top $k$ relevant ones for each input.
* **Load Balancing**: Training techniques (like Gaussian noise) ensure the router doesn't overfit on just one expert.



---

## 3. Deployment Trends: SLMs & Parallelism
The shift toward faster and more localized models has introduced new generative paradigms and optimization tricks.

### Small Language Models (SLMs)
Techniques used to run models on "edge devices" like phones:
1.  **Knowledge Distillation**: A "Teacher" model trains a smaller "Student" by transferring its prediction logic.
2.  **Pruning**: Removing redundant parameters that don't impact the final output.
3.  **Quantization**: Reducing numerical precision (e.g., to 4-bit) to save memory.

### Diffusion LLMs
An experimental approach (e.g., the **Mercury** model) that generates the entire response in parallel through a denoising process. 
* **Speed**: Can reach generation rates of over 1,000 tokens per second, far exceeding standard auto-regressive models.

---

## 4. Summary Table: Optimization Tradeoffs

| Technique | Goal | Resource Impact |
| :--- | :--- | :--- |
| **KV Caching** | TPOT Latency | Increases Memory Usage  |
| **Quantization** | Model Size | Decreases Accuracy/Robustness  |
| **Static Batching** | Throughput | Increases TTFT Latency  |
| **MoE** | Quality/Speed | Increases Total Disk/VRAM footprint  |

***
### 👉 Next in chronological order: To be continued...