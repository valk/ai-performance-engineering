# LLM Training & Fine-Tuning

## Agenda
* **LLM Training Phases**: Pre-training, Fine-tuning, and Alignment
* **Transformer Architectures**: Decoders, Encoders, and Encoder-Decoders
* **Data for Training**: Sources, Quality Filtering, and Legal Challenges
* **Self-Supervised Learning & Loss Functions**
* **Scaling Laws for Large Models**
* **Why Fine-tune?**: Adaptation vs. Retrieval
* **Full Parameter Fine-tuning vs. PEFT**
* **LoRA**: Low-Rank Adaptation
* **QLoRA**: Efficiency through Quantization


## LLM Training Phases
The development of an LLM is generally divided into three major steps:

1.  **Pre-training**: Building the model from scratch on enormous, diverse datasets to learn general language patterns.
2.  **Fine-tuning**: Adapting an existing model to a specific task (e.g., summarization) or domain (e.g., healthcare).
3.  **Alignment**: Final tuning for safety, ethical behavior, and human preference (often using RLHF).



## Transformer Architectures Recap
Models are optimized for different behaviors based on their structure:

* **Encoders (Masked Language Models)**: Predict missing words from surrounding context on both sides; often used for classification.
* **Decoders (Causal/Autoregressive)**: Predict tokens from left to right, one at a time; excellent for text generation.
* **Encoder-Decoders**: Map one sequence to another; highly popular for translation and speech-to-text.


## Training Mechanics: Data & Loss
### The Data Mix
Models are trained on vast amounts of text where the proportion of data type matters:
* **Academics**: PubMed, arXiv, and academic papers.
* **Web**: Wikipedia, StackExchange, and general web scrapes.
* **Books & Code**: Bibliotik, GitHub, and mathematical data.

### The Loss Function
Training relies on **Cross-Entropy Loss**:
* **Self-Supervised Setup**: The model uses the next (or missing) word as its own label.
* **Teacher Forcing**: During decoder training, the model is always given the correct previous token at each step $t$, regardless of its own prediction.


## Scaling Laws
Model performance (Loss $L$) is a predictable function of parameters ($N$), dataset size ($D$), and compute budget ($C$):
* When any two factors are held constant, performance scales exponentially with the third.
* **GPT-5.5 Scale**: Training likely involved trillions of parameters and 50,000 GPUs, costing roughly $100M–$300M.


## Why Fine-tune?
Pre-trained models are powerful but may lack expertise in specific domains or languages that were rare in their training data.
* **Domain Specific**: Specializing in healthcare, finance, or legal terminology.
* **Task Specific**: Improving performance in summarization or sentiment analysis.
* **Fine-tuning vs. RAG**: RAG is excellent for grounding in facts, but fine-tuning is better for shaping core behavior, consistency, and reducing inference costs.


## Parameter-Efficient Fine-Tuning (PEFT)
Full parameter tuning updates all model weights, which is expensive and risky (memory-intensive and prone to "catastrophic forgetting"). PEFT updates only a small subset of parameters.

### LoRA (Low-Rank Adaptation)
LoRA freezes original weights and updates a low-rank approximation instead.
* **Math Logic**: Any weight matrix $W$ can be decomposed into $B \times A$.
* **Efficiency**: Updating two smaller matrices (rank 1 or 2) uses significantly fewer parameters than updating the original dense matrix.
* **Advantages**: Much faster, requires less GPU memory, and preserves original knowledge.





## QLoRA: Quantized Efficiency
QLoRA is an extended version of LoRA that quantizes the precision of network parameters to save even more memory.
* **Quantization**: Splitting a range of numbers into "buckets" (e.g., converting 32-bit floats to 4-bit NormalFloat).
* **Double Quantization**: Quantizing the quantization constants themselves to further reduce the memory footprint.
* **4-bit NormalFloat (NF4)**: An enhanced method that creates equally sized buckets to represent data distributions more accurately.



## Summary of Training Outcomes
Fine-tuning results in a new model with updated weights. By using PEFT methods like LoRA:
* A 10B parameter model can be tuned with ~40GB of VRAM instead of ~160GB.
* The model learns specific instruction formats (e.g., child vs. expert) while retaining base capabilities.

***

### Final Recap
Training an LLM moves from general acquisition (**Pre-training**) to task specialization (**Fine-tuning**) and human-centric safety (**Alignment**). Methods like **LoRA** and **QLoRA** make this high-level adaptation accessible even on limited infrastructure.

***

### 👉 Next in chronological order: [More than LLMs](More_than_LLMs.md)
