"""
    This file is part of pyandex-disk.

    pyandex-disk is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    pyandex-disk is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with pyandex-disk. If not, see <https://www.gnu.org/licenses/>. 
"""

from . import errors


def get_error_by_status_code(code):
    return {
        401: errors.UnauthorizedError,
        403: errors.ForbiddenError,
        409: errors.DiskPathError,
        404: errors.NotFoundError,
        412: errors.PreconditionFailed,
        413: errors.PayloadTooLarge,
        500: errors.InternalServerError,
        503: errors.ServiceUnavailable,
        507: errors.InsufficientStorageError,
    }.get(code)
