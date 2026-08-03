from __future__ import annotations
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response


class ReadinessPlugin:
    name = "readiness_plugin"
    required_tasks: tuple[str, ...] | None = None

    def attach_router(self, app: FastAPI) -> None:
        @app.get("/readiness")
        async def readiness(raw_request: Request):
            try :
                model_executor = raw_request.app.state.openai_serving_chat.engine.engine.model_executor
                model_runner = model_executor.driver_worker.model_runner

                # check if model weight are loaded in gpu memory
                model_weights = model_runner.model_memory_usage

                # check if KV cache has been set up
                num_cpu_blocks = model_runner.num_cpu_blocks
                num_gpu_blocks = model_runner.num_gpu_blocks

                if model_weights > 0 and num_cpu_blocks > 0  and num_gpu_blocks > 0 :
                    return Response(status_code=200)
            except: HTTPException(status_code=500, detail="Model not loaded yet or KV cache not setup yet")

    async def init_state(self, engine_client, state, args) -> None:
        state.engine_client = engine_client