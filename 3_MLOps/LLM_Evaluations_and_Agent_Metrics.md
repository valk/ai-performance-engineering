# LLM Evaluations and Agent Metrics

### Agenda
- Overview of the LLM Evaluation Problem
- Use-Case Dependent Metrics Design
- The Four Core Dimensions of LLM Metrics
- Context Length and Reasoning Constraints
- Hands-on Evaluation: Hallucination/Faithfulness Testing with Llama 3.3
- Inconsistencies and Ground Truth Realities
- Introduction to Agent Evaluation

## The Core Challenge of LLM Evaluation
- Unlike traditional machine learning tasks (MLOps) where classifications belong to rigid categorical boxes, a single prompt fed into an LLM can generate 100 entirely different, unique responses that are all perfectly high-quality and valid.
- Evaluating generic language output requires breaking away from purely deterministic static testing; it must be completely customized based on the direct parameters of your specific production use case.

## Metric Balancing Framework
When designing an expert prompt-based evaluator, production engineers must balance four foundational vectors:
- **Complexity**: Keep tasks highly localized. Do not cluster multi-step execution logic or check hundreds of criteria within a single prompt. Ensure that a human could explicitly track the rules provided to the model judge.
- **Context Length**: Limit the evaluation chunk size. While frontier models comfortably publish context limits of up to 1 million tokens, actual model reasoning performance heavily degrades once context crosses roughly 10,000 tokens. Models struggle with high-order reasoning over multi-sentence combinations as sequence length expands.
- **Accuracy & Consistency**: Address non-determinism by deploying majority vote protocols. Running the evaluator multiple times (e.g., 3 to 5 times) stabilizes results and uncovers inconsistent boundary cases.
- **Efficiency**: Keep chains lightweight. Packaging too many iterative tasks per step will massively inflate token compute costs and cause immediate VRAM bottlenecks.

## Hallucination Detection & Faithfulness
- **Groundedness / Faithfulness**: This evaluation aspect targets whether the text output produced by an AI system is entirely supported by and extracted from the raw input context.
- **The Ground Truth Trap**: Data scientists cannot blindly trust golden benchmark datasets or human annotators. Production profiling regularly uncovers data points where the human labeler was mathematically incorrect or fundamentally misinterpreted the text, highlighting the need for a programmatic swarm of fine-grained evaluators.

***

