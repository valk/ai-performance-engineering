# Topics

- Neural Networks and Multi-Layer Perceptrons (MLPs)
- Activation functions and Backpropagation
- Learned representations and Word Embeddings (Word2Vec)
- Sentence Embeddings (Concatenation, Autoencoders, Pooling)

## Neural Networks & Multi-Layer Perceptrons (MLP)
- Logistic regression is limited because it can only learn linear relationships between attributes.
- Neural networks add hidden layers and non-linear activation functions to learn complex, non-linear relationships.
- Networks with multiple layers are often called Multi-Layer Perceptrons (MLP) or Feed-Forward Neural Networks (FNN).
- The number of input features dictates the size of the input layer, and the number of desired classes dictates the size of the output layer.

### Key insights
- **Logistic regression is fundamentally just a one-layer neural network**.
- **Hidden dimensions are generally designed to be smaller than the input dimension.** This forces the network to learn condensed interactions between existing features rather than breaking them down further.

## Activation Functions & Backpropagation
- Non-linear activation functions must be cheaply computed and differentiable so they can be optimized using gradient descent.
- Common activation functions include **Sigmoid** (ranges 0 to 1, often used for probability in the final layer), **Tanh** (ranges -1 to 1), and **ReLU** (zeroes out negative values).
- **Backpropagation** utilizes the mathematical chaining rule on a computational graph to calculate derivatives across layers, allowing the optimizer to update all weights and biases simultaneously.

### Key insights
- **Lower layers learn basic concepts, higher layers learn specific concepts.** In deep neural networks, lower layers capture raw, basic features (like edges in an image), while higher layers capture highly sophisticated, problem-specific features (like distinct facial features).

## Word Embeddings & Word2Vec
- **Word embeddings** move beyond tabular one-hot encodings by transforming text into fixed-size dense vectors that capture semantics, syntax, and sentiment.
- The training relies on the **distributional hypothesis**: words appearing in similar contexts share similar meanings.
- **Word2Vec** uses a sliding window across text to maximize the likelihood of a central word given its context or predicting the context given a central word (Skip-gram).
- **Negative sampling** speeds up training and penalizes unreal contexts by pulling the target word closer to its actual context words while pushing it away from a small, randomly sampled subset of unrelated vocabulary words.

### Key insights
- **Embeddings enable mathematical meaning:** Because they are numerical vectors, you can perform semantic arithmetic. For example, the vector for "king" minus "man" plus "woman" results in a vector closest to "queen".
- **The Polysemy Problem:** Classical word embeddings result in a fixed dictionary, meaning they cannot differentiate between words with multiple meanings (e.g., "bank" as a financial institution versus the "bank" of a river).

## Sentence Embeddings
- To classify entire documents, individual word embeddings must be aggregated into sentence-level representations.
- **Concatenation** stacks word vectors, but requires a predetermined fixed input length. This forces shorter sentences to be padded and longer sentences to be truncated, resulting in lost information.
- **Autoencoders** are special networks that attempt to predict their exact input on the output side. By using a smaller hidden layer in the middle (a bottleneck), the latent space creates a highly condensed representation of the input.
- **Pooling** (such as Max or Average pooling) maps a sequence of varying lengths back into a fixed-size vector by taking the maximal or average values across dimensions.

### Key insights
- **Sentence representations power modern search:** Converting text sequences into dense vectors is the foundational step for Retrieval-Augmented Generation (RAG), where document chunks and user queries are embedded to perform cosine similarity searches.
- **Loss of structural order:** Simple methods like pooling lose the structural order of words in a sentence, an issue that is ultimately resolved by moving to sequential models like Transformers.

***

### 👉 Next: [Neural Networks and Learned Representations](../2_LLM_Architecture/Sequences_Tokenization_Attention.md)