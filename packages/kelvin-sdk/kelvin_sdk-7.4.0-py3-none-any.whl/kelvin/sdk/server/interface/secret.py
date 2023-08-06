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

from ..models.parameter_models import SecretCreateRequest, SecretDeleteRequest
from ..models.router import KelvinSDKServerRouter

router = KelvinSDKServerRouter(
    prefix="/secrets",
    tags=["Secrets - [kelvin secrets]"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def secret_list(query: Optional[str] = None) -> OperationResponse:
    """
    List all the available secrets on the Platform.
    """
    from kelvin.sdk.interface import secret_list as _secret_list

    return _secret_list(query=query, should_display=False)


@router.post("")
def secret_create(secret_create_request: SecretCreateRequest) -> OperationResponse:
    """
    Create a secret on the platform.
    """
    from kelvin.sdk.interface import secret_create as _secret_create

    return _secret_create(secret_name=secret_create_request.secret_name, value=secret_create_request.value)


@router.delete("")
def secret_delete(secret_delete_request: SecretDeleteRequest) -> OperationResponse:
    """
    Delete secrets on the platform.
    """
    from kelvin.sdk.interface import secret_delete as _secret_delete

    return _secret_delete(secret_names=secret_delete_request.secret_names)
