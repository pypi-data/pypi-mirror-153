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

from typing import Optional

import click
from click import Choice

from kelvin.sdk.lib.configs.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.models.apps.common import ApplicationLanguage
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ApplicationFlavour, ProjectType
from kelvin.sdk.lib.utils.click_utils import AppNameWithVersionType, KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def app() -> bool:
    """
    Create, build and manage applications.

    """


@app.command(cls=KSDKCommand)
@click.argument("app_name", nargs=1, type=click.STRING)
@click.option("--description", required=False, default="", type=click.STRING, help=KSDKHelpMessages.app_description)
@click.option(
    "--app-type",
    required=False,
    show_default=True,
    type=Choice(ProjectType.app_types_as_str()),
    help=KSDKHelpMessages.app_type,
)
@click.option(
    "--flavour",
    required=False,
    show_default=True,
    type=Choice(ApplicationFlavour.as_list()),
    help=KSDKHelpMessages.flavour,
)
@click.option(
    "--app-dir",
    type=click.Path(),
    required=False,
    default=".",
    help=KSDKHelpMessages.app_dir,
)
def create(
    app_name: str,
    description: str,
    app_type: Optional[ProjectType],
    flavour: Optional[ApplicationFlavour],
    app_dir: str,
) -> bool:
    """
    Create a new application based on the specified parameters.

    """
    from kelvin.sdk.interface import app_create_from_parameters

    app_type = ProjectType(app_type)
    app_flavour = ApplicationFlavour(flavour)
    kelvin_app_lang = ApplicationLanguage.python

    return app_create_from_parameters(
        app_dir=app_dir or ".",
        app_name=app_name,
        app_description=description,
        app_type=app_type,
        app_flavour=app_flavour,
        kelvin_app_lang=kelvin_app_lang,
    ).success


@app.command(cls=KSDKCommand)
@click.option(
    "--app-dir",
    type=click.Path(exists=True),
    required=False,
    default=".",
    help=KSDKHelpMessages.app_dir,
)
@click.option("--fresh", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.fresh)
def build(app_dir: str, fresh: bool) -> bool:
    """
    Build a local application into a packaged image.

    """
    from kelvin.sdk.interface import app_build

    return app_build(app_dir=app_dir, fresh_build=fresh).success


@click.group(cls=KSDKGroup)
def images() -> bool:
    """
    Management and display of local images on the Local Application Registry.

    """


@images.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all locally built applications.

    """
    from kelvin.sdk.interface import app_images_list

    return app_images_list(should_display=True).success


@images.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=AppNameWithVersionType(version_required=True))
def remove(app_name_with_version: str) -> bool:
    """
    Remove an application from the local applications list.\n

    e.g. kelvin app images remove "test-app:1.0.0"

    """
    from kelvin.sdk.interface import app_image_remove

    return app_image_remove(app_name_with_version=app_name_with_version).success


@images.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=AppNameWithVersionType(version_required=True))
@click.option(
    "--container-dir",
    type=click.Path(),
    required=False,
    default=None,
    help=KSDKHelpMessages.app_images_unpack_container_dir,
)
@click.option(
    "--output-dir",
    type=click.Path(),
    required=True,
    help=KSDKHelpMessages.app_images_unpack_output_dir,
)
def unpack(app_name_with_version: str, container_dir: str, output_dir: str) -> bool:
    """
    Extract the content of an application from its built image into the specified directory.\n

    e.g. kelvin app images unpack "test-app:1.0.0" --output-dir=my_output_dir

    """
    from kelvin.sdk.interface import app_image_unpack

    return app_image_unpack(
        app_name_with_version=app_name_with_version, container_dir=container_dir, output_dir=output_dir
    ).success


@images.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=AppNameWithVersionType(version_required=True))
@click.argument("output_dir", nargs=1, type=click.Path())
def config(app_name_with_version: str, output_dir: str) -> bool:
    """
    Extract the app configuration file (app.yaml) from a built image into a specific directory.\n

    e.g. kelvin app images config "test-app:1.0.0" my_output_dir/

    """
    from kelvin.sdk.interface import app_image_config

    return app_image_config(app_name_with_version=app_name_with_version, output_dir=output_dir).success


app.add_command(images)
