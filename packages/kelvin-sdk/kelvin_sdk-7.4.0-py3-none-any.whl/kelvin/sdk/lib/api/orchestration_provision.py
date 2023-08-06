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

from kelvin.sdk.client.error import APIError
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.display_utils import success_colored_message
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.general_utils import ansi_escape_string
from kelvin.sdk.lib.utils.logger_utils import logger


def node_provision_script() -> OperationResponse:
    """
    Get the provisioning script to setup an node.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the node provision script.

    """
    try:
        logger.info("Retrieving the node provision script..")

        client = session_manager.login_client_on_current_url()

        provision_script = client.orchestration_provision.download_cluster_provision_script()
        script = provision_script.provision_script if provision_script.provision_script else ""
        script = success_colored_message(message=script)

        get_provision_script_warning: str = f"""\n
            # 1 - Prepare your node Host

               > Install Ubuntu 18.04 on your host.
               > The host must have at least 2GB of RAM, 10GB of Disk and a x86-64 Processor.


            # 2 - Install all necessary dependencies

               > To install and run the Kelvin Orchestration System, execute the following command on your host and
                follow the prompted instructions:

                {script}

        """
        logger.info(get_provision_script_warning)

        return OperationResponse(success=True, data=ansi_escape_string(value=script))

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving the provision script: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving the provision script: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)
