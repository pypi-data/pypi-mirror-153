"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""

from kelvin.sdk.lib.models.apps.ksdk_app_setup import ProjectCreationParametersObject
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.server.models.parameter_models import AppBuildRequest, AppImagesUnpackRequest
from kelvin.sdk.server.models.router import KelvinSDKServerRouter

apps_router = KelvinSDKServerRouter(
    prefix="/app",
    tags=["Apps - [kelvin app]"],
    responses={404: {"description": "Not found"}},
)

apps_images_router = KelvinSDKServerRouter(
    prefix="/app_images",
    tags=["App Images - [kelvin app images]"],
    responses={404: {"description": "Not found"}},
)


@apps_router.post("")
def app_create(project_creation_parameters: ProjectCreationParametersObject) -> OperationResponse:
    """
    The entry point for the creation of an application. (Parameters)

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.
    """

    from kelvin.sdk.interface import app_create as _app_create

    return _app_create(project_creation_parameters=project_creation_parameters)


@apps_router.get("/config")
def app_config(app_config_file_path: str) -> OperationResponse:
    """
    Yields the loaded json/dict for the provided configuration file path. (Parameters)

    """
    from kelvin.sdk.interface import app_config as _app_config

    return _app_config(app_config_file_path=app_config_file_path)


@apps_router.post("/build")
def app_build(app_build_request: AppBuildRequest) -> OperationResponse:
    """
    The entry point for the building of a App.

    Package the App on the provided app directory.
    """
    from kelvin.sdk.interface import app_build as _app_build

    return _app_build(app_dir=app_build_request.app_dir_absolute_path, fresh_build=app_build_request.fresh_build)


@apps_images_router.get("")
def app_images_list() -> OperationResponse:
    """
    Retrieve the list of all application images as well as its running.

    Will yield 2 tables:
        - the 1st containing the existing Apps
        - the 2nd containing all the running processes.
    """
    from kelvin.sdk.interface import app_images_list as _app_images_list

    return _app_images_list(should_display=False)


@apps_images_router.delete("/{app_name_with_version:path}")
def app_images_remove(app_name_with_version: str) -> OperationResponse:
    """
    Remove the specified application from the existing image list (in the docker instance).
    """
    from kelvin.sdk.interface import app_image_remove as _app_images_remove

    return _app_images_remove(app_name_with_version=app_name_with_version)


@apps_images_router.post("/unpack")
def app_image_unpack(app_images_unpack_request: AppImagesUnpackRequest) -> OperationResponse:
    """
    Extract the content of an application from its built image.
    """
    from kelvin.sdk.interface import app_image_unpack as _app_image_unpack

    return _app_image_unpack(
        app_name_with_version=app_images_unpack_request.app_name_with_version,
        container_dir=app_images_unpack_request.container_dir,
        output_dir=app_images_unpack_request.output_dir,
    )
