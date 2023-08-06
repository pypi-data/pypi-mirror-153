from typing import Any, Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute, APIRouter


class KelvinSDKServerRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = await original_route_handler(request)
            try:
                import json

                operation_result_successful: bool = json.loads(response.body).get("success", False)
                response.status_code = response.status_code if operation_result_successful else 400
            except Exception:
                pass
            return response

        return custom_route_handler


class KelvinSDKServerRouter(APIRouter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(route_class=KelvinSDKServerRoute, *args, **kwargs)
