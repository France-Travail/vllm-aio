from __future__ import annotations

import uuid
from typing import Iterable
from fastapi import FastAPI
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send


DEFAULT_PATHS = frozenset({
    "/v1/chat/completions",
    "/v1/completions",
    "/v1/responses",
    "/v1/models",
})

class _AddModelInstanceHeaderMiddleware:

    def __init__(
        self, 
        app: ASGIApp, 
        paths: Iterable[str] = DEFAULT_PATHS,
        header_name: str = "x-model-instance",
    ) -> None:
        self.app = app
        self.paths = frozenset(paths)
        self.header_name = header_name
    
    def _matches(self, path: str) -> bool:
        return any(p in path for p in self.paths)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or not self._matches(scope["path"]):
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                app_state = scope["app"].state
                model_instance = getattr(app_state, "model_instance", None)
                if model_instance is not None:
                    headers = MutableHeaders(raw=message["headers"])
                    headers.append(self.header_name, str(model_instance))
            await send(message)

        await self.app(scope, receive, send_wrapper)


class ModelInstancePlugin:
    name = "model_instance_plugin"
    required_tasks: tuple[str, ...] | None = ("generate",)

    def attach_router(self, app: FastAPI) -> None:
        app.add_middleware(_AddModelInstanceHeaderMiddleware)

    async def init_state(self, engine_client, state, args) -> None:
        state.model_instance = str(uuid.uuid4())