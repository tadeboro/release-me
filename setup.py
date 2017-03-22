# coding: utf-8
# Copyright (c) 2017 Tadej Borovšak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools


setuptools.setup(
    name="release-me",
    version="0.1.0",
    author="tadeboro",
    author_email="tadeboro@gmail.com",
    packages=["release_me"],
    license="LICENSE",
    description="Simple Github CLI release helper",
    install_requires=[
        "requests>=2.4.2",
    ],
    entry_points={
        "console_scripts": [
            "github-release = release_me.cli:main",
        ]
    }
)
