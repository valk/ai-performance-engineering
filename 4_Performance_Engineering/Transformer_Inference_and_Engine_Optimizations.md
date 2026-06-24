## Transformer Inference & Engine Optimizations

### Agenda
- Inference Engine Ecosystem (Beyond model.forward)
- Memory Pressure Layout: Weights, Activations, and KV Cache
- High-Level Mechanics: Prefill vs. Decode Phases
- Key Performance Metrics: TTFT, Tapot, ITL, and Goodput
- PagedAttention (vLLM Engine) Memory Architecture
- Batching Strategies: Static, Dynamic, and Continuous Batching
- CPU Scheduling, Preemption, and Prefix Caching

## Memory Footprint Architecture
Modern LLM serving optimization requires managing three main GPU memory components:
- **Weights**: Static, fixed parameter arrays loaded into High Bandwidth Memory (HBM) once at startup.
- **Activations**: Transient, dynamic mathematical tensor arrays that only exist during a token's immediate forward pass and are discarded instantly during inference since there is no backward gradient calculation.
- **KV Cache**: Stateful, continuously expanding Key-Value projections that must be preserved across autoregressive cycles so past context isn't mathematically recalculated. Long-context sequences can easily grow to dwarf the static model weights themselves.

## Prefill vs. Decode Phase Execution
- **Prefill Phase**: Computes the initial Key-Value pairs across the entire input prompt simultaneously in a parallel pass. It utilizes the GPU's processing tensor cores heavily, rendering this phase strictly **compute-bound**.
- **Decode Phase**: Generates text output autoregressively, exactly one token at a time. Every token requires fetching the complete historical KV cache matrix from VRAM, keeping arithmetic intensity low and rendering this phase **memory-bandwidth bound**.

## Engine Profiling Metrics
- **TTFT (Time to First Token)**: The duration between sending a request and receiving the initial streaming token, dictated directly by the speed of the compute-bound prefill kernel.
- **ITL (Inter-Token Latency)**: The individual duration required to compute a single standalone step during token generation.
- **Tapot (Time per Output Token)**: The average calculation speed tracking all generation cycles across an full output payload.
- **Goodput**: The volume of requests successfully completed completely inside a strict customer Service Level Agreement (SLA), as opposed to raw throughput numbers that include lagging or stalled requests.

## Memory Virtualization: PagedAttention
- Naive inference allocation requires pre-allocating large, continuous blocks of contiguous GPU memory matching the absolute maximum sequence limit, resulting in severe internal and external fragmentation (up to 60-80% waste).
- Derived from OS paging concepts, **PagedAttention** partitions the stateful KV cache into small, fixed-size logical pages stored non-contiguously in scattered physical slots. A dynamic block lookup table resolves addresses on demand, slashing memory waste to near zero and opening the hardware up for massive concurrent batches.

## Batching and CPU Scheduling Mechanics
- Traditional **Static Batching** forces concurrent requests to wait until every sequence in the execution thread completes its full generation length before returning data.
- **Continuous Batching** operates via a dynamic CPU scheduler loop that re-evaluates the active VRAM batch at every single micro-step. As soon as one request hits an EOF token, it is immediately ejected, and a newly incoming prefill prompt is dynamically slotted into the open execution blocks to maximize utilization.

***

