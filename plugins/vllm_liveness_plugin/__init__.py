from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import Response


class LivenessPlugin:
    name = "liveness_plugin"
    required_tasks: tuple[str, ...] | None = None

    def attach_router(self, app: FastAPI) -> None:
        @app.get("/liveness")
        async def liveness(raw_request: Request):
            await raw_request.app.state.engine_client.check_health()
            return Response(status_code=200)

    async def init_state(self, engine_client, state, args) -> None:
        state.engine_client = engine_client