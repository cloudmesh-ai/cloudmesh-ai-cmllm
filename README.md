# Cloudmesh AI CMLLM (Containerized Model LLM Orchestrator)

`cloudmesh-ai-cmllm` provides a unified orchestration interface for containerized AI workloads and inference runtimes. Integrated as a subcommand of the `cmx` CLI, it simplifies the deployment and management of LLMs across diverse environments, from local workstations to High-Performance Computing (HPC) clusters.

## Key Features

- **Unified CLI UX**: Manage container lifecycles using a consistent namespace (`cmx container start|stop|status`), eliminating the need to switch between native `docker` or `apptainer` commands.
- **Multi-Runtime Abstraction**: 
    - **Docker**: Optimized for local development and cloud instances.
    - **Apptainer**: Tailored for HPC environments (e.g., Rivanna) with native support for rootless execution and NVIDIA GPU pass-through (`--nv`).
- **AI-Centric Configuration**: Centralized management of GPU allocation, port mappings for API endpoints, and volume mounts for model weights and datasets.
- **Hybrid Infrastructure Target**: Run the exact same AI workflow locally in a container or on a remote HPC cluster by simply swapping the `--runtime` flag.
- **Simplified GPU Pass-through**: Intelligent handling of GPU device allocation (e.g., `all`, `0`, `1,2`) across different container backends.

## Quick Start

### 1. Installation

```bash
git clone https://github.com/cloudmesh-ai/cloudmesh-ai-cmllm.git
cd cloudmesh-ai-cmllm
pip install -e .
```

### 2. Basic Usage

#### Start an AI Inference Container (e.g., vLLM)
```bash
# Start a vLLM container using Docker with GPU support
cmx container start --image vllm/vllm-openai:latest --gpus all -p 8000:8000

# Start the same workload on an HPC cluster using Apptainer
cmx container start --image vllm/vllm-openai:latest --runtime apptainer -v /home/user/weights:/weights
```

#### Manage Container Lifecycle
```bash
# List active cmx-managed containers
cmx container status

# Stop and remove a container
cmx container stop cmx-service
```

## Runtime Support Matrix

| Runtime | Target Environment | GPU Support | Volume Binding | Status |
| :--- | :--- | :---: | :---: | :--- |
| **Docker** | Workstation / Cloud | ✅ (`--gpus`) | ✅ (`-v`) | 🟢 |
| **Apptainer** | HPC Clusters | ✅ (`--nv`) | ✅ (`--bind`) | 🟢 |

## Documentation

Detailed guides are available in the `/docs` folder:

- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [CLI Reference](docs/cli.md)
- [Architecture Overview](docs/architecture.md)
- [Contributing Guide](docs/contributing.md)

## Testing

The project ensures stability across different runtimes using a tiered testing strategy:

- **Unit Tests**: Verify CLI parsing and command generation logic using mocks.
- **Integration Tests**: End-to-end validation of container startup and status checks on systems with Docker/Apptainer installed.
- **Compliance Suite**: Ensures that both Docker and Apptainer backends provide a consistent interface for the user.

## Contributing

We welcome contributions to expand the supported runtimes and AI orchestration capabilities. Please see [Contributing](docs/contributing.md) for guidelines.
