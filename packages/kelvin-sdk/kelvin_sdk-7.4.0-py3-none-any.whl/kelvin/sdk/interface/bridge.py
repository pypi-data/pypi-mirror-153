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

from typeguard import typechecked

from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def bridge_list(should_display: bool = False) -> OperationResponse:
    """
    List all available bridges in the platform.

    Parameters
    ----------
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the bridges available on the platform.

    """
    from kelvin.sdk.lib.api.bridge import bridge_list as _bridge_list

    return _bridge_list(query=None, should_display=should_display)


@typechecked
def bridge_search(query: str, should_display: bool = False) -> OperationResponse:
    """
    Search for specific bridges based on a query.

    Parameters
    ----------
    query : str
        The query to search for.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the matching bridges available on the platform.

    """
    from kelvin.sdk.lib.api.bridge import bridge_list as _bridge_list

    return _bridge_list(query=query, should_display=should_display)


@typechecked
def bridge_show(bridge_name: str, should_display: bool = False) -> OperationResponse:
    """
    Show the details of a bridge.

    Parameters
    ----------
    bridge_name : str
        The name of the bridge.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the yielded bridge instance and its detailed data.

    """
    from kelvin.sdk.lib.api.bridge import bridge_show as _bridge_show

    return _bridge_show(bridge_name=bridge_name, should_display=should_display)


@typechecked
def bridge_assets(bridge_name: str, should_display: bool = False) -> OperationResponse:
    """
    List all assets associated with a specific bridge.

    Parameters
    ----------
    bridge_name : str
        The name of the bridge.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating assets associated with a specific bridge.

    """
    from kelvin.sdk.lib.api.bridge import bridge_assets as _bridge_assets

    return _bridge_assets(bridge_name=bridge_name, should_display=should_display)


@typechecked
def bridge_streams(bridge_name: str, should_display: bool = False) -> OperationResponse:
    """
    List all data streams associated with a specific bridge.

    Parameters
    ----------
    bridge_name : str
        The name of the bridge.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating data streams associated with a specific bridge.

    """
    from kelvin.sdk.lib.api.bridge import bridge_streams as _bridge_streams

    return _bridge_streams(bridge_name=bridge_name, should_display=should_display)


@typechecked
def bridge_metrics(bridge_name: str, should_display: bool = False) -> OperationResponse:
    """
    List all metrics associated with a specific bridge.

    Parameters
    ----------
    bridge_name : str
        The name of the bridge.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating metrics associated with a specific bridge.

    """
    from kelvin.sdk.lib.api.bridge import bridge_metrics as _bridge_metrics

    return _bridge_metrics(bridge_name=bridge_name, should_display=should_display)
