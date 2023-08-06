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

from kelvin.sdk.lib.configs.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def schema() -> bool:
    """
    General schema operations.
    """


@schema.command(cls=KSDKCommand)
@click.argument("file_path", nargs=1, type=click.Path(exists=True))
@click.option("--schema-file", type=click.Path(exists=True), required=False, help=KSDKHelpMessages.schema_file)
def validate(file_path: str, schema_file: Optional[str]) -> bool:
    """
    Validate a file against a schema.

    """
    from kelvin.sdk.interface import schema_validate

    return schema_validate(file_path=file_path, schema_file_path=schema_file, full_schema_errors=True).success
