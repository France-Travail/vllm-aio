# vLLM-AIO (All-In-One)

This repository provides an extended, production-ready Docker image for [vLLM](https://github.com/vllm-project/vllm) — a high-throughput and memory-efficient LLM serving engine. 

Building upon the official vLLM base image, **vLLM-AIO** introduces two major enhancements:
1. **Audio Support:** Pre-installs all necessary dependencies for audio processing (`vllm[audio]`).
2. **On-the-fly Plugins:** Features a plug-and-play architecture to easily add, manage, and load custom FastAPI endpoint plugins dynamically at startup.

---

## Repository Structure

This project uses a monorepo approach for custom plugins. All plugins share a single configuration file (`pyproject.toml`) and are automatically discovered during the Docker build.

```text
vllm-aio/
├── Dockerfile
├── scripts/
    ├── setup_venv.sh         # Install the repo. in local
├── pyproject.toml            # Centralized config and plugin entry points
├── .github/workflows/
│   └── publish.yaml          # CI/CD to push the image to GHCR
└── plugins/                  # Drop your custom plugins here
    ├── vllm_custom_1_endpoint_plugin/
    │   └── __init__.py
    └── vllm_another_custom_endpoint_plugin/
        └── __init__.py
```

---

## How to Add a New Plugin

Adding a new custom endpoint to your vLLM server is straightforward:

1. **Create your plugin folder:** Add a new folder inside the `plugins/` directory (e.g., `plugins/my_new_plugin/`) and write your Python code (usually starting with `__init__.py`).
2. **Register the entry point:** Open `pyproject.toml` and register your plugin under the `[project.entry-points."vllm.endpoint_plugins"]` section:

```toml
[project.entry-points."vllm.endpoint_plugins"]
arguments_api = "vllm_arguments_endpoint_plugin:ArgumentsEndpointPlugin"
my_new_api = "my_new_plugin:MyPluginClass"
```

*Note: The `[tool.setuptools.packages.find]` configuration in `pyproject.toml` will automatically discover your new folder inside `plugins/`. No need to list it manually!*

---

## Local Development & Testing

If you want to develop or test your plugins locally without building the Docker image every time, you can use the provided setup script. It will create an isolated virtual environment and install vLLM along with your custom plugins in editable mode.

```bash
# 1. Create a venv and activate it
python -m venv my_venv
source my_venv/bin/activate

# 2. Run the setup script to setup the environment
sh scripts/setup_venv.sh

# 3. Start the local server with your plugins enabled
export VLLM_PLUGINS="arguments_api"
vllm serve /path/to/your/local/model \
  --served-model-name your-model-name \
  --trust-remote-code
```

## Links and Acknowledgements
* **vLLM Official Repository:** [github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
* **vLLM Plugin Documentation:** [Endpoint Plugins Design](https://docs.vllm.ai/en/stable/design/endpoint_plugins.html)