from http import HTTPStatus
from typing import Optional, Tuple, Any, Dict
import requests
from urllib.parse import urlparse
import logging

from arthurai.client.validation import validate_response_status
from arthurai.common.exceptions import UserValueError, ArthurInternalError, ForbiddenError
from arthurai.core.auth_info import AuthInfo

JSON_CONTENT_TYPE = "application/json"

logger = logging.getLogger(__name__)


def construct_url(*parts: str, validate=True, default_https=True) -> str:
    """Construct a url from various parts

    Useful for joining pieces which may or may not have leading and/or trailing
    slashes. e.g. construct_url("http://arthur.ai/", "/api/v3", "/users") will yield the same valid url as
    construct_url("http://arthur.ai", "api/v3/", "users/").

    :param validate: if True, validate that the URL is valid
    :param default_https: if True, allow urls without a scheme and use https by default
    :param parts: strings from which to construct the url
    :return: a fully joined url
    """
    # join parts
    url = '/'.join(s.strip('/') for s in parts)

    # add scheme
    parsed_url = urlparse(url)
    if parsed_url.scheme is None or parsed_url.scheme == "":
        if default_https:
            logger.warning("No url scheme provided, defaulting to https")
            url = "https://" + url
            parsed_url = urlparse(url)
        elif validate:
            raise UserValueError(f"No scheme provided in URL {url}")

    # validate
    if validate and (parsed_url.scheme is None or parsed_url.scheme == ""
                     or parsed_url.netloc is None or parsed_url.netloc == ""):
        joiner = "', '"
        raise UserValueError(f"Invalid url, cannot construct URL from parts '{joiner.join(parts)}'")

    return url


def get_current_org(api_http_host: str, api_prefix: str, access_key: str, verify_ssl: bool = True) \
        -> Optional[str]:
    """Get the current organization for the provided access key

    :param api_http_host: base url of the host to connect to, including protocol (e.g. "https://app.arthur.ai")
    :param api_prefix: prefix of the API to connect to (e.g. "/api/v3")
    :param access_key: API Key to pass to the API
    :param verify_ssl: Boolean for whether requests should verify that the SSL certificate is valid and not self-signed
    :return: the organization ID associated with the provided access key, None if no such organization exists
    """
    try:
        internal_user_org = get_arthur_internal_user_org(api_http_host, api_prefix, access_key, verify_ssl)
    except ForbiddenError:
        auth_info = get_auth_info(api_http_host, api_prefix, access_key, verify_ssl)
        if auth_info is None:
            raise ArthurInternalError("Invalid / non-existent auth_info")
        elif len(auth_info.organization_ids) == 1:
            # If the user is authenticated into a single org, automatically select it as the user's current org
            return auth_info.organization_ids[0]
        elif len(auth_info.organization_ids) > 1:
            # Raise exception and give the user options of available current organizations
            authenticated_org_id_str = "".join(f"{org_id}\n" for org_id in auth_info.organization_ids)[:-1]
            raise UserValueError(f"Your access_key provides access to multiple organizations - please specify one of the following:\n{authenticated_org_id_str}")
        else: # len(auth_info.organization_ids) == 0
            return None

    # Valid internal_user_org was found
    return internal_user_org


def get_auth_info(api_http_host: str, api_prefix: str, access_key: str, verify_ssl: bool = True) \
        -> Optional[AuthInfo]:
    """Get the AuthInfo struct associated with the provided access key

    :param api_http_host: base url of the host to connect to, including protocol (e.g. "https://app.arthur.ai")
    :param api_prefix: prefix of the API to connect to (e.g. "/api/v3")
    :param access_key: API token to pass to the API
    :param verify_ssl: Boolean for whether requests should verify that the SSL certificate is valid and not self-signed
    :return: the AuthInfo associated with the provided access key
    :permissions: N/A
    """
    url = construct_url(api_http_host, api_prefix, "/users/me/auth_info")
    headers = {'Authorization': access_key,
               'Accept': JSON_CONTENT_TYPE}

    try:
        resp = requests.get(url, headers=headers, verify=verify_ssl)
    except requests.RequestException as e:
        raise UserValueError(f"Failed to connect to {api_http_host}, please ensure the URL is correct") from e
    if resp.status_code == HTTPStatus.UNAUTHORIZED:
        raise UserValueError("Unauthorized, please ensure your access key is correct")
    if resp.status_code == HTTPStatus.NOT_FOUND:
        raise ArthurInternalError("Auth Info endpoint not implemented by api-host")

    validate_response_status(resp, HTTPStatus.OK)
    return AuthInfo.from_json(resp.text)


def get_arthur_internal_user_org(api_http_host: str, api_prefix: str, access_key: str, verify_ssl: bool = True) \
        -> Optional[str]:
    """Get the current organization for the provided Arthur access key belonging to an Arthur internal user

    :param api_http_host: base url of the host to connect to, including protocol (e.g. "https://app.arthur.ai")
    :param api_prefix: prefix of the API to connect to (e.g. "/api/v3")
    :param access_key: API Key to pass to the API
    :param verify_ssl: Boolean for whether requests should verify that the SSL certificate is valid and not self-signed
    :return: the organization ID associated with the provided access key, None if no such organization exists
    :permissions: N/A
    """
    url = construct_url(api_http_host, api_prefix, "/users/me")
    headers = {'Authorization': access_key,
               'Accept': JSON_CONTENT_TYPE}

    try:
        resp = requests.get(url, headers=headers, verify=verify_ssl)
    except requests.RequestException as e:
        raise UserValueError(f"Failed to connect to {api_http_host}, please ensure the URL is correct") from e
    if resp.status_code == HTTPStatus.UNAUTHORIZED:
        raise UserValueError("Unauthorized, please ensure your access key is correct")
    if resp.status_code == HTTPStatus.FORBIDDEN:
        # The only case in which /users/me would return a Forbidden error response is if the calling user
        # is not an Arthur internal user (e.g. using a 3rd party identity provider)
        raise ForbiddenError("Caller is not an Arthur internal user")
    validate_response_status(resp, HTTPStatus.OK)
    response_body = resp.json()
    return response_body.get("organization_id", None)


def user_login(api_http_host: str, api_prefix: str, login: str, password: str, verify_ssl: bool = True) \
        -> Tuple[str, Dict[str, Any]]:
    """Get the current organization for the provided access key

    :param api_http_host: base url of the host to connect to, including protocol (e.g. "https://app.arthur.ai")
    :param api_prefix: prefix of the API to connect to (e.g. "/api/v3")
    :param login: the username or password to use to log in
    :param password: password for the user
    :param verify_ssl: Boolean for whether requests should verify that the SSL certificate is valid and not self-signed
    :return: a tuple of (access_key, {user object})
    """
    url = construct_url(api_http_host, api_prefix, "/login")
    headers = {'Accept': JSON_CONTENT_TYPE}
    body = {'login': login,
            'password': password}
    try:
        resp = requests.post(url, headers=headers, json=body, verify=verify_ssl)
    except requests.RequestException as e:
        raise UserValueError(f"Failed to connect to {api_http_host}, please ensure the URL is correct") from e
    if resp.status_code == HTTPStatus.UNAUTHORIZED:
        raise UserValueError(f"Unauthorized, please ensure your username and password are correct")

    validate_response_status(resp, HTTPStatus.OK)

    return resp.cookies.get('Authorization'), resp.json()
