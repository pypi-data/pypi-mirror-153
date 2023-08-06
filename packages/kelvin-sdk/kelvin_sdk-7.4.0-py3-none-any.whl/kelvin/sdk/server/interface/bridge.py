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
from kelvin.sdk.server.models.router import KelvinSDKServerRouter

router = KelvinSDKServerRouter(
    prefix="/bridges",
    tags=["Bridges - [kelvin bridge]"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def bridge_list(query: Optional[str] = None) -> OperationResponse:
    """
    List all available bridges in the platform.
    """
    if query:
        from kelvin.sdk.interface import bridge_search as _bridge_search

        return _bridge_search(query=query, should_display=False)
    else:
        from kelvin.sdk.interface import bridge_list as _bridge_list

        return _bridge_list(should_display=False)


@router.get("/{bridge_name}")
def bridge_show(bridge_name: str) -> OperationResponse:
    """
    Show the details of a bridge.
    """
    from kelvin.sdk.interface import bridge_show as _bridge_show

    return _bridge_show(bridge_name=bridge_name, should_display=False)


@router.get("/{bridge_name}/assets")
def bridge_assets(bridge_name: str) -> OperationResponse:
    """
    List all assets associated with a specific bridge.
    """
    from kelvin.sdk.interface import bridge_assets as _bridge_assets

    return _bridge_assets(bridge_name=bridge_name, should_display=False)


@router.get("/{bridge_name}/streams")
def bridge_streams(bridge_name: str) -> OperationResponse:
    """
    List all data streams associated with a specific bridge.
    """
    from kelvin.sdk.interface import bridge_streams as _bridge_streams

    return _bridge_streams(bridge_name=bridge_name, should_display=False)


@router.get("/{bridge_name}/metrics")
def bridge_metrics(bridge_name: str) -> OperationResponse:
    """
    List all metrics associated with a specific bridge.
    """
    from kelvin.sdk.interface import bridge_metrics as _bridge_metrics

    return _bridge_metrics(bridge_name=bridge_name, should_display=False)
