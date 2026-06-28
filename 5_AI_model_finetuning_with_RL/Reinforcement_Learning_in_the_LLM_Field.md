## 5. AI model finetuning with RL: Reinforcement Learning in the LLM Field

### Agenda
- Traditional Pipeline: Pre-training vs. Supervised Fine-Tuning (SFT)
- Limitations and Objective Mismatch of SFT
- Core Reinforcement Learning Setup for Transformers
- RLHF vs. Verifiable Reinforcement Learning (RLVR)
- The 3 Pillars of Reinforcement Learning From Human Feedback
- Reward Modeling, Sigmoid-Log Losses, and KL Regularization
- PPO Pipeline Heavy Infrastructure vs. Direct Policy Optimization (DPO)

## The Pre-Training and SFT Foundation
- **Pre-Training Stage:** Models learn language syntax and foundational information from vast, unsupervised web corpora via standard cross-entropy next-token prediction objectives.
- **Supervised Fine-Tuning (SFT) Stage:** Adapts a pre-trained model to accept instructional formatting and adopt an explicit response style by training it exclusively on high-quality, human-curated prompt-and-target pairings.

## The Mismatch Limitation of SFT
- **Objective Mismatch Paradox:** The mathematical objective of SFT is simply to replicate the training dataset token-by-token using token cross-entropy. It lacks an inherent optimization mechanism to score an open-ended, creative response or ensure the code passes exact executable metrics.
- **Data Blindspots and Hallucination Triggering:** SFT exposes the neural model to a single explicit absolute answer trajectory per prompt. When the model is forced to output responses outside its real knowledge bounds, it introduces structural hallucination behaviors.

## Transforming Transformers into Reinforcement Agents
To optimize behaviors directly rather than mimicking strings, text generation is contextualized within standard Reinforcement Learning components:
- **State ($S$):** The text string prompt provided to the interface.
- **Action ($A$):** The generated token text response outputted by the model.
- **Policy ($pi$):** The weights and architectural distribution of the LLM itself.
- **Reward ($R$):** A continuous scalar assessment scoring the quality of an output.

## The Three Steps of RLHF

[ SFT Initial Model ] ──> [ Collect Preference Pairs ] ──> [ Train Reward Model ] ──> [ Policy Optimization ]

1. **Initial SFT Anchor:** Begin with a stable, instruction-tuned base model.
2. **Preference Gathering:** Collect ranking arrays across duplicate generations where human judges or advanced synthetic systems evaluate outputs to select a preferred winner ($y_w$) and a rejected loser ($y_l$).
3. **Reward Model Fitting:** Fine-tune a distinct model to ingest the prompt/answer pairings and return a continuous scalar performance score matching the specified formatting.

## Reward Model Fitting Loss Mechanics
The standard reward network uses a binary cross-entropy formulation over paired preference data:
$$mathcal{L}_{RM}(theta) = -mathbb{E}_{(x, y_w, y_l) sim D} left[ log sigma left( r_theta(x, y_w) - r_theta(x, y_l) right) right]$$
- If the network ranks the chosen winning text $y_w$ higher than the bad answer output $y_l$, the scalar gap expands cleanly, reducing the overall penalty.
- If the network places a higher weight value on the lower-ranked response, the score becomes negative, resulting in a steep loss penalty.

## The Vulnerability of Reward Hacking and KL Regularization
- **Reward Hacking:** Without strict constraints, optimization policies alter their underlying parameters to maximize numerical reward functions via counterproductive generation habits (such as structural length bias, where models excessively padding answers get over-rewarded because human evaluation data inherently correlates long length with thoroughness).
- **Kullback-Leibler (KL) Divergence:** Keeps the updated policy close to the initial distribution of the SFT base anchor by applying a penalty whenever token probability scales drift too far from the reference model.

## Optimization Architecture Paths: PPO vs. DPO

### Proximal Policy Optimization (PPO)
The traditional, multi-stage reinforcement design framework leveraged heavily in pioneering AI systems. It is resource-heavy and requires running and maintaining up to four large distinct transformer instances simultaneously in active infrastructure memory:
1. **The Active Policy Model:** The target network receiving adjustments.
2. **The Reference Model:** A frozen copy used to calculate token-level KL divergence.
3. **The Reward Model:** The proxy scoring engine.
4. **The Value Model:** An additional baseline estimator used to optimize convergence trajectories.

### Direct Policy Optimization (DPO)
A simpler alternative developed at Stanford that eliminates the need to train a separate reward model or sample text during training.
- **The Core Math Trick:** Re-parameterizes the standard alignment objective function to solve the optimization directly using log probabilities extracted from the current policy versus the frozen base SFT reference model.
- **Infrastructure Impact:** Reduces runtime training complexity by maintaining only two models concurrently in compute memory (the active policy and the frozen base reference). This lowers infrastructure overhead and accelerates alignment workflows for text and coding applications.
