ARG VLLM_VERSION_IMAGE
FROM vllm/vllm-openai:v${VLLM_VERSION_IMAGE}

ARG VLLM_VERSION_IMAGE
RUN uv pip install --system vllm[audio]==${VLLM_VERSION_IMAGE}

WORKDIR /opt/vllm-aio
COPY pyproject.toml ./
COPY plugins/ ./plugins/
RUN uv pip install --system .

# List all plugins with a simple comma
ENV VLLM_PLUGINS="liveness_api,readiness_api"

ENTRYPOINT ["vllm", "serve"]