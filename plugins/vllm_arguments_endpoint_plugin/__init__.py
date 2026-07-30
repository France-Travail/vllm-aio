from __future__ import annotations
from typing import Callable
from fastapi import FastAPI, Request


class ArgumentsEndpointPlugin:
    name = "agurments_endpoint_plugin"
    required_tasks: tuple[str, ...] | None = None

    def attach_router(self, app: FastAPI) -> None:
        @app.get("/plugins/get_arguments")
        async def get_arguments(raw_request: Request):
            arguments = raw_request.app.state.arguments
            return {"arguments": arguments}

    async def init_state(self, engine_client, state, args) -> None:
        state.arguments = {
            key: value.__name__ if isinstance(value, Callable) else value
            for key, value in vars(args).items()
        }