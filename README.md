# Nebius AI Performance Engineering

This project contains my notes for a comprehensive set of materials, guides, and exercises from Nebius for AI Performance Engineering course.

I'm updating it as I go through the course.

## Modules

### 1. From AI Model to AI Product
Explore how to transition from raw machine learning models to functional AI-driven products.

*   **[Intro to AI & LLMs](1_From_AI_model_to_AI_product/Intro_to_AI_&_LLMs.md)**: An essential introduction to the landscape of Large Language Models. This module covers:
    *   What changed with LLMs and their core limitations.
    *   The GPT assistant training pipeline (Pretraining, SFT, RLHF).
    *   Tokenization strategies and token economics.
    *   Prompt and Context engineering techniques, including Zero-shot, Few-shot, and Chain-of-Thought prompting.
    *   Practical insights into tool use and function calling.

*   **[Evaluation & Benchmarks](1_From_AI_model_to_AI_product/Evaluation_&_Benchmarks.md)**: An essential introduction to the landscape of Large Language Models. This module covers:
    *   Why LLM evaluation is hard
    *   Evaluation metrics
    *   Evaluation-Driven Development (EDD) - the mindset
    *   Common metrics and where they break
    *   Common benchmarks and their expiration dates
    *   LLM-as-a-Judge and automated behavioral evals (Anthropic's Bloom)
    *   Human evaluation
    *   EDD in practice: turning metrics into decisions

* [AI Systems & Test-Time Compute](1_From_AI_model_to_AI_product/AI_Systems_&_Test-Time_Compute.md)
    - Fine-Tuning vs Retrieval Augmented Generation (RAG)
    - The RAG Pipeline Components
    - Chunking and Embedding strategies
    - Evaluating RAG Systems and the "RAG Triad"
    - Evaluation Datasets and Benchmarks


### 2. LLM Architecture
Deep dive into the underlying architecture of modern LLMs.

*   [LLM Architecture - AI and LLM Intro](2_LLM_Architecture/AI_and_LLM_Intro.md)
    - Intro and Generative Al Landscape
    - Types of ML
    - Supervised Tasks Evaluation
    - Language Models
    - N-Gram LM
    - Language Models Evaluation

* [AI Model Training](2_LLM_Architecture/AI_Model_Training.md)
    - Core Terminology & Hierarchy
    - Language Model Architectures
    - Optimization & Regularization
    - Evaluation & Benchmarks

* [Neural Networks and Learned Representations](2_LLM_Architecture/Neural_Networks_and_Learned_Representations.md)
    - Neural Networks and Multi-Layer Perceptrons (MLPs)
    - Activation functions and Backpropagation
    - Learned representations and Word Embeddings (Word2Vec)
    - Sentence Embeddings (Concatenation, Autoencoders, Pooling)

* [Sequences, Tokenization, Attention](2_LLM_Architecture/Sequences_Tokenization_Attention.md)
    - Standardization and Pre-processing
    - Character-Level vs. Word-Level Tokenization
    - Subword Tokenization (BPE, WordPiece, SentencePiece)
    - Domain-Specific Tokenization in Healthcare and Hebrew
    - Recurrent Neural Networks (RNN) and Sequential Data
    - RNN Architectures: Acceptors, Transducers, and Encoder-Decoders

* [Transformers and LLMs](2_LLM_Architecture/Transformers_and_LLMs.md)
    - Contextualized vs. Static Embeddings
    - The Transformer Architecture: Encoder and Decoder
    - Self-Attention and Multi-Head Attention
    - Training "Tricks": Skip Connections, Normalization, and Dropout
    - Positional Encodings
    - LLM Architectures: Encoder-Only, Decoder-Only, and Encoder-Decoder
    - Inference Techniques: Top-K, Top-P, and Temperature

* [LLM Training](2_LLM_Architecture/LLM_Training.md)
    - LLM Training Phases
    - Transformer Architectures
    - Training Mechanics: Data & Loss
    - Scaling Laws
    - Why Fine-tune?
    - Parameter-Efficient Fine-Tuning (PEFT)
    - LoRA (Low-Rank Adaptation)
    - QLoRA: Quantized Efficiency

* [More than LLMs](2_LLM_Architecture/More_than_LLMs.md)
    - Efficient LLMs at Inference Time
    - New LLM Architectures
    - Deployment Trends: SLMs & Parallelism
    - Summary Table: Optimization Tradeoffs

### 3. MLOps
Best practices for deploying, monitoring, and maintaining machine learning models in production.

*   **[E2E ML Pipelines and Infrastructure Case Study](3_MLOps/E2E_ML_Pipelines_and_Infrastructure_Case_Study.md)**: This module covers: * Designing end-to-end ML pipelines. * Infrastructure considerations for scalable ML deployments. * Monitoring and maintaining deployed models.

*   **[Vector Databases and Storage Optimization for ML](3_MLOps/Vector_Databases_and_Storage_Optimization_for_ML.md)**: This module covers: * Vector database architectures. * Storage optimization strategies for machine learning workloads. * Query performance and scalability.

*   **[LLM Evaluations and Agent Metrics](3_MLOps/LLM_Evaluations_and_Agent_Metrics.md)**: This module covers: * Metrics for evaluating large language models. * Assessment techniques for AI agents. * Benchmarking methodologies.

### 4. Performance Engineering
Techniques for optimizing model inference, reducing latency, and managing compute resources efficiently.

*   **[Speculative Decoding](4_Performance_Engineering/Speculative_Decoding.md)**: This module covers: * Speculative decoding techniques. * Inference optimizations. * Real-world performance gains.

*   **[Transformer Inference and Engine Optimizations](4_Performance_Engineering/Transformer_Inference_and_Engine_Optimizations.md)**: This module covers: * Efficient transformer inference methods. * Engine optimizations for latency reduction. * Hardware considerations for inference acceleration.

### 5. AI Model Finetuning with RL
Advanced topics in model refinement using Reinforcement Learning.

*   **[Reinforcement Learning in the LLM Field](5_AI_model_finetuning_with_RL/Reinforcement_Learning_in_the_LLM_Field.md)**: This module covers: * RL fundamentals in LLM fine-tuning. * Reward modeling for language generation. * Advanced RL techniques like PPO for LLM alignment.

## Colabs

- [LLM Architecture - AI and LLM Intro](https://colab.research.google.com/drive/1QhgH6HqXerRrHBElhTeJqwNamG9fE_NW?usp=sharing)