ARG VLLM_IMAGE_TAG=0.26.0
FROM vllm/vllm-openai:v${VLLM_IMAGE_TAG}

RUN uv pip install --system vllm[audio]==${VLLM_IMAGE_TAG}

WORKDIR /opt/vllm-aio
COPY pyproject.toml ./
COPY plugins/ ./plugins/
RUN uv pip install --system .

# List all plugins with a simple comma
ENV VLLM_PLUGINS="arguments_api"

ENTRYPOINT ["vllm", "serve"]
