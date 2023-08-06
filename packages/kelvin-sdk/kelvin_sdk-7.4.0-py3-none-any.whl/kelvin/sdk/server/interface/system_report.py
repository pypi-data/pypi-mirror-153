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
    prefix="/report",
    tags=["Host machine report - [kelvin report]"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def kelvin_report(app_config_absolute_path: Optional[str] = None) -> OperationResponse:
    """
    Report the user's system information and log records for support purposes.
    """
    from kelvin.sdk.interface import kelvin_support_report as _kelvin_support_report

    return _kelvin_support_report(app_config=app_config_absolute_path, generate_report_file=False)
