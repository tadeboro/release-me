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

from __future__ import print_function

from . import client

import pkg_resources
import argparse
import json
import sys


def get_client(token):
    try:
        c = client.GithubClient(token)
    except client.GithubClientError as e:
        print("ERROR: {}".format(e.msg))
        sys.exit(1)
    return c


def check_repo(c, repo):
    repo_exists, _ = c.get_repo(repo)
    if not repo_exists:
        print("ERROR: invalid repo '{}'".format(args.repo))
        sys.exit(1)


def create_release(args):
    """
    Create new Github release.
    """
    c = get_client(args.token)
    check_repo(c, args.repo)

    notes = args.notes.read()
    created, r = c.create_release(args.repo, args.tag, notes)
    if not created:
        print("Error:\n'{}'".format(json.dumps(r, indent=2)))
        sys.exit(1)


def delete_release(args):
    """
    Delete Github release
    """
    c = get_client(args.token)
    check_repo(c, args.repo)
    success, release = c.get_release(args.repo, args.tag)
    if not success:
        print("Error: release '{}' not found.".format(args.tag))
        sys.exit(1)

    deleted, r = c.delete_release(args.repo, release["id"])
    print(json.dumps(release, indent=2))
    if not deleted:
        print("Error:\n'{}'".format(json.dumps(r, indent=2)))
        sys.exit(1)


def add_common_params(parser):
    parser.add_argument("--token", required=True,
                        help="Github OAuth token")
    parser.add_argument("--repo", required=True,
                        help="Github repo (eg. tadeboro/release-me)")
    parser.add_argument("--tag", required=True,
                        help="Existing git tag name")


def create_parser():
    parser = argparse.ArgumentParser(description="Github release helper")
    parser.add_argument(
        "--version", action="version",
        version=pkg_resources.get_distribution("release_me").version
    )

    subparsers = parser.add_subparsers()

    create_p = subparsers.add_parser("create",
                                     description=create_release.__doc__)
    create_p.add_argument("--notes", required=True,
                          type=argparse.FileType("r"),
                          help="Path to release notes file")
    create_p.set_defaults(func=create_release)
    add_common_params(create_p)

    delete_p = subparsers.add_parser("delete")
    delete_p.set_defaults(func=delete_release)
    add_common_params(delete_p)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)
