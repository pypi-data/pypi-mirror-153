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

from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.server.models.parameter_models import SchemaValidateRequest
from kelvin.sdk.server.models.router import KelvinSDKServerRouter

router = KelvinSDKServerRouter(
    prefix="/schema",
    tags=["Schema - [kelvin schema]"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def schema_get(schema_file_path: Optional[str] = None) -> OperationResponse:
    """
    Expose the the content of a schema.
    If no path is provided, yields back the latest schema version.
    """
    from kelvin.sdk.interface import schema_get as _schema_get

    return _schema_get(schema_file_path=schema_file_path)


@router.post("/validate")
def schema_validate(schema_validate_request: SchemaValidateRequest) -> OperationResponse:
    """
    Validate a file against a schema.
    """
    from kelvin.sdk.interface import schema_validate as _schema_validate

    return _schema_validate(
        file_path=schema_validate_request.file_path,
        schema_file_path=schema_validate_request.schema_file_path,
        full_schema_errors=schema_validate_request.full_schema_errors,
    )
