import pathlib
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from ..lib.configs.kelvin_sdk_server import KelvinSDKServerConfigs

# 1 - Construct the supported routers
from ..lib.models.operation import OperationResponse
from .interface import (
    app,
    appregistry,
    asset,
    asset_type,
    authentication,
    bridge,
    configuration,
    datatype,
    emulation,
    node,
    schema,
    secret,
    system_report,
    workload,
)

supported_routers = [
    app.apps_router,
    app.apps_images_router,
    appregistry.router,
    asset.router,
    asset_type.router,
    authentication.router,
    bridge.router,
    configuration.router,
    datatype.router,
    emulation.router,
    node.router,
    schema.router,
    secret.router,
    system_report.router,
    workload.router,
]

# 2 - Initialise the FastAPI object and setup the supported routers
kelvin_server = FastAPI(
    title=KelvinSDKServerConfigs.kelvin_server_title, description=str(KelvinSDKServerConfigs.kelvin_server_description)
)
for router in supported_routers:
    kelvin_server.include_router(router=router)

# 3 - Setup the structure of the FastAPI
current_directory = pathlib.Path(__file__).parent.resolve()
ui_directory = current_directory / KelvinSDKServerConfigs.kelvin_server_structure_ui_dir
templates_directory = ui_directory / KelvinSDKServerConfigs.kelvin_server_structure_templates_dir
static_directory = ui_directory / KelvinSDKServerConfigs.kelvin_server_structure_static_dir

templates = Jinja2Templates(directory=str(templates_directory))
kelvin_server.mount(
    "/static",
    StaticFiles(directory=static_directory),
    name="static",
)


@kelvin_server.get("/", response_class=HTMLResponse, tags=["Landing page"])
async def root(request: Request) -> Any:
    from kelvin.sdk.cli.version import version as _version

    return templates.TemplateResponse("main.html", {"request": request, "version": _version})


@kelvin_server.get("/info", tags=["System Information"])
async def info() -> OperationResponse:
    from kelvin.sdk.interface import kelvin_system_information as _kelvin_system_information

    return _kelvin_system_information(display=False)


@kelvin_server.get("/version", tags=["Kelvin SDK version"])
async def version() -> dict:
    from kelvin.sdk.cli.version import version as _version

    return {"version": _version}
