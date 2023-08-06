import requests as req
from typing import Optional, Union


def get_resource(
    url: str,
    params: Optional[dict] = None,
    timeout: int = 10
    ) -> req.Response:
    """Returns a response object.

    Parameters:
        url (str): a url that specifies the resource.
        params (dict): optional dictionary of querystring arguments.
        timeout (int): timeout value in seconds

    Returns:
        Response: contains a server’s response to an HTTP request.
    """
    if params:
        return req.get(url, params, timeout=timeout)
    else:
        return req.get(url, timeout=timeout)


def get_resource_json(
    url: str,
    params: Optional[dict] = None,
    timeout: int = 10
    ) -> Union[dict, list]:
    """Returns a response object decoded into a dictionary or list.

    Parameters:
        url (str): a url that specifies the resource.
        params (dict): optional dictionary of querystring arguments.
        timeout (int): timeout value in seconds

    Returns:
        dict | list: dictionary or list representation of the decoded JSON.
    """
    return get_resource(url, params, timeout=timeout).json()