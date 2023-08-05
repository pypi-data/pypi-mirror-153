"""
    This file is part of pyandex-disk.

    pyandex-disk is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    pyandex-disk is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with pyandex-disk. If not, see <https://www.gnu.org/licenses/>. 
"""

import logging

import requests

from . import errors
from . import utils


logger = logging.Logger("pyandex_disk")

OK_STATUSES = {
    "STATUS_OK": 200,
    "STATUS_CREATED": 201,
    "STATUS_ACCEPTED": 202,
    "STATUS_NO_CONTENT": 204,
}

DISK_URL = "https://cloud-api.yandex.net/v1"


class Requester:

    def __init__(self, token):
        self._token = token

    def get(self, url, params=None, **kwargs):
        return self.wrap(requests.get)(url=url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.wrap(requests.post)(url=url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.wrap(requests.put)(url=url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.wrap(requests.patch)(url=url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.wrap(requests.delete)(url=url, **kwargs)

    def wrap(self, method):
        """
        - Add extra headers to request
        - Change url
        - Handle response status code
        """
        method_name = {
            requests.get: "GET",
            requests.post: "POST",
            requests.put: "PUT",
            requests.patch: "PATCH",
            requests.delete: "DELETE",
        }[method]

        def wrapped(url: str, *args, **kwargs):
            absolute_url = kwargs.pop("absolute_url", False)
            if not absolute_url:
                url = "{}/{}".format(DISK_URL, url.lstrip("/"))

            if not kwargs.get("headers"):
                kwargs["headers"] = {}
            if not kwargs.get("params"):
                kwargs["params"] = {}

            if "overwrite" in kwargs:
                kwargs["overwrite"] = "true" if kwargs["overwrite"] else "false"
            if "params" in kwargs and "overwrite" in kwargs["params"]:
                kwargs["params"]["overwrite"] = "true" if kwargs["params"]["overwrite"] else "false"

            logger.debug("Call {!r} method by url={!r}".format(method_name, url))
            if kwargs.pop("without_auth", False) is not True:
                kwargs["headers"]["Authorization"] = "OAuth {}".format(self._token)
            response = method(url, *args, **kwargs)
            logger.debug("Response status_code={} by url={}/{}".format(
                response.status_code,
                url,
                method_name
            ))
            if response.status_code in OK_STATUSES.values():
                return response

            try:
                response_msg = response.json()["message"]
            except ValueError:
                response_msg = str(response.content)

            logger.error(
                "Status_code={}; response body: {}; request_url={!r}; method={!r}".format(
                    response.status_code,
                    response_msg,
                    response.url,
                    method_name,
                )
            )

            # handle status code
            exc = utils.get_error_by_status_code(response.status_code)
            if exc is None:
                raise errors.RequestError(response_msg)
            raise exc(response_msg)

        return wrapped
