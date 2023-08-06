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
from typing import Tuple

import click

from kelvin.sdk.lib.configs.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def datatype() -> bool:
    """
    Manage and view data types.

    """


@datatype.command(cls=KSDKCommand, name="list")
@click.option("all_datatypes", "--all", is_flag=True, show_default=True, help=KSDKHelpMessages.datatype_list_all)
def list_datatypes(all_datatypes: bool) -> bool:
    """
    List the data types available on the platform.

    """
    from kelvin.sdk.interface import datatype_list

    return datatype_list(all_datatypes=all_datatypes, should_display=True).success


@datatype.command(cls=KSDKCommand)
@click.argument("query", type=click.STRING, nargs=1)
def search(query: str) -> bool:
    """
    Search for specific data types available on the platform.

    e.g. kelvin datatype search "my.type"
    """
    from kelvin.sdk.interface import datatype_search

    return datatype_search(query=query, should_display=True).success


@datatype.command(cls=KSDKCommand)
@click.argument("data_type", type=click.STRING, nargs=1)
@click.option(
    "--output-dir",
    type=click.STRING,
    help=KSDKHelpMessages.datatype_create_output_dir,
)
def create(data_type: str, output_dir: str) -> bool:
    """
    Create a basic data type spec file from the provided name.

    e.g. kelvin datatype create "my.type"
    """
    from kelvin.sdk.interface import datatype_create

    return datatype_create(datatype_name=data_type, output_dir=output_dir).success


@datatype.command(cls=KSDKCommand)
@click.argument("name_with_version", type=click.STRING, nargs=1)
def show(name_with_version: str) -> bool:
    """
    Displays the details on a specific datatype.

    e.g. kelvin datatype show "my.type:1.0.0"
    """
    from kelvin.sdk.interface import datatype_show

    return datatype_show(datatype_name_with_version=name_with_version, should_display=True).success


@datatype.command(cls=KSDKCommand)
@click.option(
    "--input-dir",
    type=click.STRING,
    help=KSDKHelpMessages.datatype_upload_input_dir,
)
@click.option(
    "datatypes",
    "--names",
    type=click.STRING,
    multiple=True,
    required=False,
    help=KSDKHelpMessages.datatype_upload_names,
)
def upload(input_dir: str, datatypes: Tuple[str]) -> bool:
    """
    Upload data types to the platform.

    e.g. kelvin datatype upload --names=my.type:1.0.0
    """
    from kelvin.sdk.interface import datatype_upload

    # transform into list and remove duplicates
    clean_datatypes = list(set(datatypes))
    return datatype_upload(input_dir=input_dir, datatypes=clean_datatypes).success


@datatype.command(cls=KSDKCommand)
@click.argument("name_with_version", type=click.STRING, nargs=1)
@click.option(
    "--output-dir",
    type=click.STRING,
    help=KSDKHelpMessages.datatype_download_output_dir,
)
def download(name_with_version: str, output_dir: str) -> bool:
    """
    Download a data type from the platform.

    e.g. kelvin datatype download "my.type:1.0.0" --output-dir=my_dir/
    """
    from kelvin.sdk.interface import datatype_download

    return datatype_download(datatype_name_with_version=name_with_version, output_dir=output_dir).success
