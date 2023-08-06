import json
from typing import List

from charset_normalizer import api
from keycloak.exceptions import KeycloakError

from kelvin.sdk.client.error import APIError


def retrieve_error_message_from_api_exception(api_error: APIError) -> str:
    """Returns the 'pretty' error message from the APIError.

    Parameters
    ----------
    api_error : APIError
         The exception yielded by the service call.

    Returns
    -------
    str:
        a string containing the error message of the APIError.

    """
    try:
        error_messages: List[str] = []
        api_errors = api_error.errors
        for error in api_errors:
            if error.http_status_code and error.http_status_code == 403:
                no_permission_error_message: str = """\n
                    You don’t have the required permissions to execute this command.\n
                    Please contact your system administrator. \n
                """
                return no_permission_error_message
            if error.message:
                error_message = error.message
                if isinstance(error_message, list):
                    error_messages.append("; ".join(item for item in error_message))
                else:
                    error_messages.append(str(error_message))
            elif error.description:
                error_messages.append(error.description)

        message = "; ".join(error_messages)
        return f"(API error) {message}"

    except Exception as exc:
        return f"Error retrieving APIError - {str(exc)}"


def retrieve_error_message_from_keycloak_exception(keycloak_exception: KeycloakError) -> str:
    """Returns the 'pretty' error message from the KeycloakError.

    Parameters
    ----------
    keycloak_exception : KeycloakError
        The exception yielded by the service call.

    Returns
    -------
    str:
        a string containing the error message of the KeycloakError.

    """
    try:
        try:
            message = json.loads(keycloak_exception.error_message)
        except (UnicodeDecodeError, AttributeError):
            message = {"error_description": "Error retrieving KeyCloak exception"}

        return f"(Authentication API error) {message.get('error_description')}"

    except Exception as exc:
        return f"Error handling KeycloakError exception - {str(exc)}"
