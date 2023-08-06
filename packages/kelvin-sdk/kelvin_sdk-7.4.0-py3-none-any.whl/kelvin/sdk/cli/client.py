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

from typing import Sequence

import click

from kelvin.sdk.lib.utils.click_utils import KSDKCommand


@click.command(cls=KSDKCommand)
@click.argument("args", type=click.STRING, nargs=-1)
def client(args: Sequence[str]) -> bool:
    """
    Launch an IPython session ready to access data on the platform.

    """
    from kelvin.sdk.interface.client import client as _client

    _client(args=args)

    return True
