"""
    This file is part of pyandex-disk.

    pyandex-disk is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    pyandex-disk is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with pyandex-disk. If not, see <https://www.gnu.org/licenses/>. 
"""

import pathlib
import setuptools


setuptools.setup(
    name="pyandex_disk",
    description="Python HTTP API wrapper for Yandex Disk.",
    version="1.0.0-alpha",
    author="Mikhail Volkov, leestarb",
    author_email="freylis2@gmail.com",
    maintainer="leestarb",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires = [
        "requests >= 2.9.1",
    ],
)
