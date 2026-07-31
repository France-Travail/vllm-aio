VLLM_VERSION="$(cat VLLM_VERSION | tr -d '[:space:]')"

pip install --upgrade pip uv

echo "== Installing vLLM ${VLLM_VERSION} (match the Dockerfile's version!) =="
uv pip install vllm[audio]==${VLLM_VERSION}

echo "== Installing the custom endpoint plugin in editable mode =="
uv pip install -e .