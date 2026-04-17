# Topics

- Fine-Tuning vs Retrieval Augmented Generation (RAG)
- The RAG Pipeline Components
- Chunking and Embedding strategies
- Evaluating RAG Systems and the "RAG Triad"
- Evaluation Datasets and Benchmarks

## Fine-Tuning vs RAG
- Fine-tuning is primarily for teaching the model language, style, tone, and structure 
rather than specific facts.
- RAG solves the context and data problem, providing the model with private or 
updated information that it did not see during training.
- While fine-tuning is like a parrot spending a lot of time reading in a library, RAG is 
like giving the parrot a smart search engine to query the library on demand.

### Key insights
- Language models should not be viewed as creatures holding vast amounts of correct factual
 knowledge, but rather as having the capability to understand when and where to apply 
 provided information.
- A common misconception is that having a large dataset automatically means you should
 fine-tune; if the goal is factual accuracy, RAG is the appropriate solution.

## The RAG Pipeline Components
- Pre-processing (Step 0): Parsing complex document formats like PDFs, HTML, or images into text.
- Indexing (Offline): Segmenting text into chunks, running them through an embedding model, and
 storing the vectors in a database.
- Retrieval (Online): Converting a user's query into an embedding, searching the vector
 database, and returning the top-K most similar chunks.
- Augmented Generation (Online): Injecting the retrieved chunks into a prompt alongside
 grounding instructions for the LLM to generate an answer.

### Key insights
- Interestingly, according to Yuval, parsing PDFs remains an extremely difficult problem,
especially when dealing with complex structures like tables or right-to-left languages like
Hebrew and Arabic, and that's what I spent a few month with pretty good success.
- The retrieval component is the primary bottleneck in RAG; if the system retrieves garbage,
the generation will also be garbage.

## Chunking and Embedding
- Chunking breaks large documents into manageable segments (such as fixed size, adaptive,
or sentence-level) to maintain semantic clarity.
- Overlapping chunks is a standard practice to prevent context from being lost at the cut-off
 boundaries.
- Embedding models convert text chunks into numerical dimensions, allowing the system to measure
 semantic similarity using metrics like Cosine Similarity.

### Key insights
- Smaller chunk sizes provide granular context but enlarge the database, whereas larger chunk
 sizes risk losing the specific details.
- Adding metadata (like document source, date, or a brief summary) to chunks greatly improves
 the flexibility and accuracy of the retrieval step.
- There is no single optimal chunk size for all queries; experimenting with multiple chunk sizes
 and combining their retrieval results can significantly boost performance.

## Evaluating RAG Systems
- Evaluation must target both the end-to-end system quality and the individual components to
 allow for proper debugging.
- The RAG Triad consists of measuring Context Relevance (did it retrieve the right docs?),
 Faithfulness (is the answer grounded purely in the context?), and Answer Relevance (does it
 actually address the user's query?).
- Retrieval quality is generally measured by Context Recall, testing if the system successfully
 fetched all necessary ground-truth documents.

### Key insights
- If the retrieval step fails, the entire system fails, because the generation model is denied
 the context it needs to provide a grounded answer.
- Measuring precision in retrieval is flawed because the score artificially fluctuates depending
 on the chosen "K" (number of retrieved chunks) parameter.
- Increasing the amount of retrieved context improves Recall, but blindly optimizing for Recall
 can introduce noise and decrease the overall system correctness.

## Evaluation Datasets and Benchmarks
- Synthetic datasets are the cheapest way to evaluate, using an LLM to generate test questions
 and answers based on your chunks.
- Semi-synthetic datasets use real user logs and support tickets, relying on LLMs to label which
 chunk answers the query.
- Human annotation remains the most accurate and reliable way to create a golden dataset, though
 it is the most expensive.
- Domain-specific benchmarks like FinanceBench or Legal RAG Bench exist to test RAG pipelines.

### Key insights
- Synthetic dataset generation carries the flawed assumption that every question can be answered
 by a single, local chunk of text.
- Standard RAG benchmarks rarely correlate with real-world success because real data is
 significantly messier than benchmark data.
- Benchmark creators often design highly contrived "multi-hop" trivia questions that real
 enterprise
 users would never actually ask.

***

### 👉 Next in module: []()

### 👉 Next in chronological order: [Neural_Networks_and_Learned_Representations](../2_LLM_Architecture/Neural_Networks_and_Learned_Representations.md)