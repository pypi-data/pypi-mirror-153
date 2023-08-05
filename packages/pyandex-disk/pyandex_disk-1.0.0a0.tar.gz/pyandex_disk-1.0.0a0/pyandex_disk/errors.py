"""
    This file is part of pyandex-disk.

    pyandex-disk is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    pyandex-disk is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with pyandex-disk. If not, see <https://www.gnu.org/licenses/>. 
"""

class YandexDiskError(Exception):
    pass


class UnauthorizedError(YandexDiskError):
    pass


class ForbiddenError(YandexDiskError):
    pass


class DiskPathError(YandexDiskError):
    pass


class NotFoundError(YandexDiskError):
    pass


class RequestError(YandexDiskError):
    pass


class PreconditionFailed(YandexDiskError):
    pass


class PayloadTooLarge(YandexDiskError):
    pass


class ServerError(YandexDiskError):
    pass


class InternalServerError(ServerError):
    pass


class ServiceUnavailable(ServerError):
    pass


class InsufficientStorageError(YandexDiskError):
    pass
