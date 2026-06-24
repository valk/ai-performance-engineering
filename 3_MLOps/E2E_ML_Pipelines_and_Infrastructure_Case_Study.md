# E2E ML Pipelines and Infrastructure Case Study


### Agenda
* **Pipeline Engines & Orchestration**: The transition from manual scripts to Directed Acyclic Graphs (DAGs).
* **Apache Airflow In-Depth**: Core components, deployment modes, and programmatic configuration.
* **ML vs. Data Engineering Workloads**: Specialized modular blocks within production systems.
* **Nebius R&D Infrastructure Case Study**: Multi-region GPU computing, preemption strategies, observability configurations, and managing shared research clusters.

---

## THE ORCHESTRATION LAYER: SCRIPTS TO DIRECTED ACYCLIC GRAPHS (DAGs)

## The Evolution of Production Orchestration


* **The Problem with Imperative Automation**: Managing machine learning tasks via naive shell scripts creates brittle operational flows. Traditional linear scripts rely on hardcoded parameters, lack checkpoint-restart awareness, execute tasks in strict serial order, and force massive GPU clusters to sit idle during non-GPU data preparation phases.
* **The Directed Acyclic Graph (DAG)**: Transforming detached task scripts into a unified workflow graph creates a predictable topology. In this model, steps execute concurrently or sequentially based on strict data-dependency rules.

##### Workflow Topology Mapping
````txt
                  ┌───────────────┐
                  │Train/Test Split│
                  └───────┬───────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
   ┌──────────────────┐      ┌──────────────────┐
   │Prepare Train Data│      │Prepare Test Data │
   └─────────┬────────┘      └─────────┬────────┘
             ▼                         │
     ┌──────────────┐                  │
     │ Model Train  │                  │
     └───────┬──────┘                  │
             ▼                         ▼
   ┌────────────────────────────────────────────┐
   │             Model Evaluation               │
   └────────────────────────────────────────────┘
````

* **The Role of MLOps**: The primary mission of MLOps is to abstract underlying compute resources, map logical step progressions into deterministic executions, handle retries automatically at the point of failure, and provide reliable replication frameworks across large shared server clusters.

---

## APACHE AIRFLOW IN-DEPTH

Apache Airflow serves as an open-source workflow orchestration management engine. Initially built for data engineering pipelines, it has evolved into an effective orchestrator for multi-tier machine learning tasks.

### Core Architecture Components
Airflow organizes workflow execution across five separate system tiers:

##### Architecture Node Communication
````txt
                  ┌──────────────┐
                  │ Web Server   │ ◄─── User Interface / API
                  └──────┬───────┘
                         │
  ┌──────────────┐       ▼       ┌────────────────┐
  │  Scheduler   │◄─────────────►│ Metadata Store │
  └──────┬───────┘               │   (PostgreSQL) │
         │                       └────────────────┘
         ▼
  ┌──────────────┐
  │ Worker Array │ ───► Executes Pipeline Steps as Isolated Pods
  └──────────────┘
````

1. **Python SDK**: A programmatic framework used to build and configure complex workflow topologies using native Python code as a configuration language.
2. **Web Server**: A clean web portal and API surface used to trigger runs, pass JSON parameters, check system logs, and review run history.
3. **Scheduler**: The core coordination controller that continuously reads active graph definitions, tracks task states, and cues pending workloads.
4. **Metadata Store**: A database backend (typically PostgreSQL) that records state changes, user definitions, and historical metrics.
5. **Worker Execution Layer**: The infrastructure tier where pipeline tasks are executed. In large production clusters, this layer runs tasks as isolated containers via the Kubernetes Executor.

### Programmatic DAG Configuration

* **Declarative Representation**: Python code in Airflow acts strictly as a front-end configuration script. The workflow management engine reads these definition scripts, translates them into internal structural configuration representations, and renders execution chains based on explicit routing operators:

##### Dependency Code Snippet
````txt
# Programmatic definition of parallel and sequential task dependencies
data_split >> [prepare_train_data, prepare_test_data]
prepare_train_data >> model_training
[model_training, prepare_test_data] >> model_evaluation
````

---

## Deployment and Code Synchronization

### Deployment Archetypes
* **Standalone Mode**: Runs all architectural components (scheduler, web server, local database, and workers) inside a single local thread configuration. This setup is useful for local prototyping and personal development environments, but is not suitable for scale-out production.
* **Kubernetes Native (Helm Deployment)**: The standard enterprise production configuration. Orchestrated via standardized Helm deployment routines (`helm install airflow`), this model spins up a decoupled cluster architecture where every single task step executes as an isolated container pod on demand.

### Code Sync Mechanics in Containerized Infrastructure

##### Sync Pipeline Schema
````txt
  [Git Repository] ───► Git-Sync Sidecar (Every minute) ───► [/dags Shared Volume] ───► Airflow Workers
````

* **Git-Sync Architecture**: A sidecar loop process runs inside the worker containers, checking the upstream repository every minute to pull down active graph definitions and write them directly into a shared runtime volume.
* **Object Store Sync**: An alternative approach where automated CI pipelines bundle updated workflow definitions and push them to a secure object storage bucket (S3), triggering an automatic refresh across active worker components.
* **Monolithic Image Packing**: The most predictable and secure production strategy. Every workflow definition file is compiled directly into the master Docker image used to deploy the Airflow cluster. While this guarantees structural consistency, it requires a full container redeployment for every pipeline modification.

---

## END-TO-END WORKLOAD BLOCK TYPOLOGIES

Production ML environments partition pipeline steps into distinct architectural blocks, mapping tailored compute hardware to individual execution phases:

##### Pipeline Block Specifications
````txt
  ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
  │ Data Processing │ ───►  │ Model Training  │ ───►  │ Model Inference │ ───►  │ Evaluation Loop │
  └─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
         │                         │                         │                         │
  • Input: Raw Files        • Input: Features         • Input: Live Queries     • Input: Predictions
  • Output: Features        • Output: Weights File    • Output: Inference Log   • Output: Metrics
  • Infrastructure:         • Infrastructure:         • Infrastructure:         • Infrastructure:
    Multi-node CPU            Multi-GPU Clusters        Decoupled Triton/vLLM     Secure Sandboxes
    Clusters (Spark)          (Torch, Jax, NCCL)        Serving Pods              (LLM-as-a-Judge)
````

---

## CASE STUDY: NEBIUS R&D INFRASTRUCTURE

## High-Performance Multi-Region Computing
The case study examines real-world production configurations deployed inside the AI research and development department, supporting more than 20 core researchers and integrating multiple specialized infrastructure components.

##### Monorepo Deployment Matrix
````txt
  ┌────────────────────────────────────────────────────────────────────────┐
  │                         Python Monorepo (GitHub)                       │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │             Global Kubernetes Mesh Layer (Nebius Cloud Compute)        │
  ├────────────────────────┬───────────────────────┬───────────────────────┤
  │     Finland Cluster    │     France Cluster    │   Kansas City Cluster │
  └────────────────────────┴───────────────────────┴───────────────────────┘
````

* **Unified Monorepo Architecture**: All application components—including training frameworks, high-throughput inference engines, batch-processing routines, and orchestrations—are managed inside a single Python monorepo. Continuous Integration workflows target bare-metal cloud servers with native GPU connections to run hardware-dependent integration tests before deployment.
* **Global Grid Coordination**: Compute resources run across an open regional grid spanning separate international infrastructure environments, such as Finland, France, and Kansas City. Researchers target execution locations explicitly at submission time to optimize hardware usage and bypass regional capacity shortages.

---

## Advanced Compute and Preemption Optimization

The infrastructure maximizes utilization by mixing two primary GPU acquisition models: **Static Allocations** (guaranteed unthrottled hardware paths) and **Preemptable Allocations** (low-cost, highly volatile instances that can be reclaimed by the cloud provider instantly).

##### Inter-Cluster Resource Eviction
````txt
   Low-Priority Workloads (Inference Pods)  ◄─── [Preempted & Evicted] ───┐
                                                                          │
   High-Priority Workloads (Multi-node Distributed Training) ─────────────┴──► Secures Infiniband Interconnect
````

* **Resilience Frameworks**: To withstand the volatility of preemptable instances, all workloads implement strict checkpoint-recovery loops and timeout handlers, allowing training states to resume seamlessly following sudden server evictions.
* **Dynamic Inter-Cluster Preemption**: When a high-priority distributed training job spins up, the cluster controller automatically evicts lower-priority inference containers. This reclaims host resources and frees up critical high-speed Infiniband connections for the multi-node training run.
* **Gang Scheduling (Volcano/Kubeflow)**: Traditional Kubernetes schedulers handle containers as isolated entities, which can cause deadlocks during distributed training runs if a cluster only partially provisions a job's required workers. To prevent this, the team deploys Volcano gang schedulers. This ensures an "all-or-nothing" allocation strategy, spinning up multi-node training runs only when all parallel worker positions can be filled simultaneously.

---

## Observability, Data Fabric, and Resource Guardrails

### Large-Scale Storage and Processing
* **YT (YTsaurus) Data Platform**: The core data fabric manages over two petabytes of research data, including raw web datasets and generated log arrays. The cluster scales out across more than 3,000 CPU cores to execute parallel MapReduce pipelines.
* **Distributed File Virtualization**: The storage platform provides a unified virtual directory layer (`/home/llm/datasets`). This allows terabyte-scale distributed data pools to look and feel like standard local directory trees to researchers, abstracting away the underlying cluster complexity.

### Monitoring Infrastructure
* **Experiment Logging**: The training loops bypass traditional basic console dumps, routing performance metrics and model loss curves directly into centralized experiment trackers like Weights & Biases or MLflow.
* **Automated Cluster Cleanup**: Research environments are prone to structural clutter, with users spinning up development environments and forgetting to tear them down. To combat this, automated cleanup routines monitor cluster activity. If an allocated model serving container shows zero inbound requests for three consecutive days, alert monitors flag the owner via Slack or trigger an automated teardown to reclaim the GPUs.

### Specialized AI Research Extensions
* **`papyrex` Training Framework**: A highly optimized internal training engine built on Google Jax, engineered explicitly to scale language model architectures efficiently across thousands of parallel GPUs.
* **`country` Security Sandbox**: A secure sandboxing platform developed in-house. It isolates untrusted code generated by running software agents, executing evaluations within hardened execution layers to protect the host infrastructure.

### 👉 Back to: [Index](../README.md)
### 👉 Next in module: [Vector Databases and Storage Optimization for ML](Vector_Databases_and_Storage_Optimization_for_ML.md)
