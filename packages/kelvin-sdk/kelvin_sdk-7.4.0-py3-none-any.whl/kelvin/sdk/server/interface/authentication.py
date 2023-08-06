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

from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.server.models.parameter_models import AuthenticationTokenRequest, LoginRequest
from kelvin.sdk.server.models.router import KelvinSDKServerRouter

router = KelvinSDKServerRouter(
    prefix="/auth",
    tags=["Authentication - [kelvin auth]"],
    responses={404: {"description": "Not found"}},
)


@router.post("/reset")
def reset() -> OperationResponse:
    """
    Reset all authentication credentials and configuration cache.
    """

    from kelvin.sdk.interface import reset as _reset

    return _reset()


@router.post("/login")
def login(login_request: LoginRequest) -> OperationResponse:
    """
    Logs the user into the provided url.
    """
    from kelvin.sdk.interface import login as _login

    return _login(
        url=login_request.url,
        username=login_request.username,
        password=login_request.password,
        totp=login_request.totp,
        reset_credentials=login_request.reset_credentials,
    )


@router.post("/logout")
def logout() -> OperationResponse:
    """
    Logs off the client all currently stored sessions.
    """
    from kelvin.sdk.interface import logout as _logout

    return _logout(ignore_destructive_warning=True)


@router.post("/token")
def authentication_token(authentication_token_request: AuthenticationTokenRequest) -> OperationResponse:
    """
    Obtain an authentication authentication_token from the API.
    """
    from kelvin.sdk.interface import authentication_token as _authentication_token

    return _authentication_token(full=authentication_token_request.full, margin=authentication_token_request.margin)
