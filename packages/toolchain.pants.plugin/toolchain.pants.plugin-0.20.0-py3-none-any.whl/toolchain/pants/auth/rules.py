# Copyright © 2019 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

# This pylint ignore is due to the migration of the pants options API, when we remove backward compatibility we should also remove this line
# pylint: disable=unexpected-keyword-arg

from __future__ import annotations

import logging
import os
import socket
import time
import uuid
import webbrowser
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from urllib.parse import urlencode

import requests
from pants.engine.console import Console
from pants.engine.environment import Environment, EnvironmentRequest
from pants.engine.fs import CreateDigest, Digest, FileContent, Workspace
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.rules import Get, collect_rules, goal_rule, rule
from pants.option.global_options import GlobalOptions
from pants.option.subsystem import Subsystem

from toolchain.pants.auth.client import ACQUIRE_TOKEN_GOAL_NAME, AuthClient, AuthError
from toolchain.pants.auth.server import AuthFlowHttpServer, TestPage
from toolchain.pants.auth.store import AuthStore
from toolchain.pants.auth.token import AuthToken
from toolchain.pants.common.network import get_common_request_headers
from toolchain.pants.common.toolchain_setup import ToolchainSetup
from toolchain.pants.common.version_helper import use_new_options
from toolchain.util.constants import REQUEST_ID_HEADER

_logger = logging.getLogger(__name__)


DEFAULT_AUTH_FILE = ".pants.d/toolchain_auth/auth_token.json"


def optional_file_option(fn: str) -> str:
    # Similar to Pant's file_option, but doesn't require the file to exist.
    return os.path.normpath(fn)


@unique
class OutputType(Enum):
    FILE = "file"
    CONSOLE = "console"


class AccessTokenAcquisitionGoalOptions(GoalSubsystem):
    name = ACQUIRE_TOKEN_GOAL_NAME
    help = "Acquires access tokens for Toolchain service."

    if use_new_options():
        from pants.option.option_types import BoolOption, EnumOption, IntOption, StrOption

        local_port = IntOption("--local-port", default=None, help="Local web server port")
        output = EnumOption(
            "--output",
            enum_type=OutputType,
            default=OutputType.FILE,
            help="Output method for access token. Outputing the console is useful if the token needs to be provided to CI",
        )
        headless = BoolOption("--headless", default=False, help="Don't open & use a browser to acquire access token")
        test_page = EnumOption(
            "--test-page",
            enum_type=TestPage,
            default=TestPage.NA,
            advanced=True,
            help="Helper to test success and error pages w/o triggering auth flow",
        )
        description = StrOption("--description", default=None, help="Token description")
    else:

        @classmethod
        def register_options(cls, register):
            super().register_options(register)
            register("--local-port", type=int, default=None, help="Local web server port")
            register(
                "--output",
                type=OutputType,
                default=OutputType.FILE,
                help="Output method for access token. Outputing the console is useful if the token needs to be provided to CI",
            )
            register("--headless", type=bool, default=False, help="Don't open & use a browser to acquire access token")
            register(
                "--test-page",
                type=TestPage,
                default=TestPage.NA,
                advanced=True,
                help="Helper to test success and error pages w/o triggering auth flow",
            )
            register("--description", type=str, default=None, help="Token description")


class AuthStoreOptions(Subsystem):
    options_scope = "auth"
    help = "Setup for authentication with Toolchain."
    if use_new_options():
        from pants.option.option_types import DictOption, IntOption, StrListOption, StrOption

        auth_file = StrOption(
            "--auth-file",
            default=DEFAULT_AUTH_FILE,
            help="Relative path (relative to the build root) for where to store and read the auth token",
        )
        from_env_var = StrOption(
            "--from-env-var", default=None, help="Loads the access token from an environment variable"
        )
        ci_env_variables = StrListOption(
            "--ci-env-variables",
            help="Environment variables in CI used to identify build (for restricted tokens)",
        )
        org = StrOption("--org", default=None, help="organization slug for public repo PRs")
        restricted_token_matches = DictOption(
            "--restricted-token-matches",
            default={},
            advanced=True,
            help="A dict containing environment variables with their expected values (regex) which need to match in order for the plugin to request a restricted access token.",
        )

        token_expiration_threshold = IntOption(
            "--token-expiration-threshold",
            default=30,
            advanced=True,
            help="Threshold (in minutes) for token TTL before plugin asks for a new token.",
        )
    else:

        @classmethod
        def register_options(cls, register):
            register(
                "--auth-file",
                default=DEFAULT_AUTH_FILE,
                type=optional_file_option,
                help="Relative path (relative to the build root) for where to store and read the auth token",
            )
            register(
                "--from-env-var", type=str, default=None, help="Loads the access token from an environment variable"
            )
            register(
                "--ci-env-variables",
                type=list,
                help="Environment variables in CI used to identify build (for restricted tokens)",
            )
            register("--org", type=str, default=None, help="organization slug for public repo PRs")
            register(
                "--restricted-token-matches",
                type=dict,
                default={},
                advanced=True,
                help="A dict containing environment variables with their expected values (regex) which need to match in order for the plugin to request a restricted access token.",
            )
            register(
                "--token-expiration-threshold",
                type=int,
                default=30,
                advanced=True,
                help="Threshold (in minutes) for token TTL before plugin asks for a new token.",
            )


class AccessTokenAcquisition(Goal):
    subsystem_cls = AccessTokenAcquisitionGoalOptions


@dataclass(frozen=True)
class AccessTokenAcquisitionOptions:
    output: OutputType
    auth_options: AuthClient
    repo_name: str
    org_name: str | None
    local_port: int | None
    headless: bool
    test_page: TestPage
    description: str

    @classmethod
    def from_options(
        cls,
        *,
        acquire_options: AccessTokenAcquisitionGoalOptions,
        store_options: AuthStoreOptions,
        pants_bin_name: str,
        repo_name: str,
        org_name: str | None,
        base_url: str,
    ) -> AccessTokenAcquisitionOptions:
        if use_new_options():
            acquire_values = acquire_options
            store_values = store_options
        else:
            acquire_values = acquire_options.options
            store_values = store_options.options
        auth_opts = AuthClient.create(
            pants_bin_name=pants_bin_name,
            base_url=f"{base_url}/api/v1",
            auth_file=store_values.auth_file,
            context="auth-acquire",
        )
        return cls(
            local_port=acquire_values.local_port,
            repo_name=repo_name,
            org_name=org_name,
            auth_options=auth_opts,
            output=acquire_values.output,
            headless=acquire_values.headless,
            test_page=acquire_values.test_page,
            description=acquire_values.description,
        )

    @property
    def log_only(self) -> bool:
        return self.output == OutputType.CONSOLE

    @property
    def ask_for_impersonation(self) -> bool:
        # For now, the console output is used when creating tokens for CI, so in that case we will also request for impersonation permissions
        # We might want to have a standalone options for that in the future, however, currently CI is the only use case for an impersonation token
        return self.log_only

    @property
    def base_url(self) -> str:
        return self.auth_options.base_url

    def get_auth_url(self, *, org: str | None, repo: str, params: dict[str, str]) -> str:
        params["repo"] = f"{org}/{repo}" if org else repo
        encoded_params = urlencode(params)
        return f"{self.base_url}/token/auth/?{encoded_params}"

    def get_token_exchange_url(self) -> str:
        return f"{self.base_url}/token/exchange/"

    @property
    def auth_file_path(self) -> Path:
        return self.auth_options.auth_file_path


@rule
async def construct_auth_store(
    auth_store_config: AuthStoreOptions,
    global_options: GlobalOptions,
    toolchain_setup: ToolchainSetup,
) -> AuthStore:
    options = auth_store_config if use_new_options() else auth_store_config.options
    environment = await Get(Environment, EnvironmentRequest(AuthStore.relevant_env_vars(options)))
    return AuthStore(
        context="rules",
        options=options,
        pants_bin_name=global_options.options.pants_bin_name,
        env=dict(environment),
        repo=toolchain_setup.safe_get_repo_name(),
        base_url=toolchain_setup.base_url,
    )


@goal_rule(desc="Acquires access token from Toolchain Web App and store it locally")
async def acquire_access_token(
    console: Console,
    workspace: Workspace,
    acquire_goal_options: AccessTokenAcquisitionGoalOptions,
    store_options: AuthStoreOptions,
    global_options: GlobalOptions,
    toolchain_setup: ToolchainSetup,
) -> AccessTokenAcquisition:
    repo_name = toolchain_setup.get_repo_name()
    acquire_options = AccessTokenAcquisitionOptions.from_options(
        pants_bin_name=global_options.options.pants_bin_name,
        acquire_options=acquire_goal_options,
        store_options=store_options,
        repo_name=repo_name,
        org_name=toolchain_setup.org_name,
        base_url=toolchain_setup.base_url,
    )
    if acquire_options.test_page != TestPage.NA:
        _test_local_server(acquire_options)
        return AccessTokenAcquisition(exit_code=0)
    try:
        auth_token = _acquire_token(console, acquire_options)
    except AuthError as error:
        console.print_stderr(str(error))
        return AccessTokenAcquisition(exit_code=-1)
    if acquire_options.log_only:
        console.print_stdout(f"Access Token is: {auth_token.access_token}")
        return AccessTokenAcquisition(exit_code=0)
    # stores token locally
    auth_file_path = acquire_options.auth_file_path
    digest = await Get(
        Digest, CreateDigest([FileContent(path=auth_file_path.name, content=auth_token.to_json_string().encode())])
    )
    workspace.write_digest(digest=digest, path_prefix=str(auth_file_path.parent))
    console.print_stdout("Access token acquired and stored.")
    return AccessTokenAcquisition(exit_code=0)


def _acquire_token(console: Console, options: AccessTokenAcquisitionOptions) -> AuthToken:
    if options.headless or not _is_browser_available():
        return _acquire_token_headless(console, options)
    return _acquire_token_with_browser(console, options)


def _test_local_server(options: AccessTokenAcquisitionOptions):
    with AuthFlowHttpServer.create_server(port=options.local_port, expected_state=str(uuid.uuid4())) as http_server:
        http_server.start_thread()
        server_url = http_server.get_test_url(options.test_page)
        success = webbrowser.open(server_url, new=1, autoraise=True)
        if not success:
            http_server.shutdown()
            raise AuthError(
                f"Failed to open web browser. {ACQUIRE_TOKEN_GOAL_NAME} can't continue.", context="auth-acquire"
            )
        time.sleep(4)  # sleep to allow the browser to load the page from the server.


def _acquire_token_with_browser(console: Console, options: AccessTokenAcquisitionOptions) -> AuthToken:
    state = str(uuid.uuid4())
    with AuthFlowHttpServer.create_server(port=options.local_port, expected_state=state) as http_server:
        http_server.start_thread()
        callback_url = http_server.server_url
        console.print_stdout(f"Local Web Server running - callback at: {callback_url}")
        params = {"redirect_uri": callback_url, "state": state}
        auth_url = options.get_auth_url(org=options.org_name, repo=options.repo_name, params=params)
        _logger.debug(f"Open Browser at: {auth_url}")
        success = webbrowser.open(auth_url, new=1, autoraise=True)
        if not success:
            http_server.shutdown()
            raise AuthError(
                f"Failed to open web browser. {ACQUIRE_TOKEN_GOAL_NAME} can't continue.", context="auth-acquire"
            )
        token_code = http_server.wait_for_code()
        desc = _get_token_desc(options)
        return _exchage_code_for_token(console, options, token_code, description=desc)


def _exchage_code_for_token(
    console: Console, options: AccessTokenAcquisitionOptions, token_code: str, description: str
) -> AuthToken:
    # TODO: Use an engine intrinsic instead of directly going to the network.
    headers = get_common_request_headers()
    data = {"code": token_code, "desc": description}
    if options.ask_for_impersonation:
        data["allow_impersonation"] = "1"
    with requests.post(options.get_token_exchange_url(), data=data, headers=headers) as response:
        if not response.ok:
            console.print_stderr(console.red(_get_error_message(response)))
            raise AuthError("Failed to acquire access token from server", context="auth-acquire")
        resp_data = response.json()
        return AuthToken.from_json_dict(resp_data)


def _acquire_token_headless(console: Console, options: AccessTokenAcquisitionOptions) -> AuthToken:
    url = options.get_auth_url(org=options.org_name, repo=options.repo_name, params={"headless": "1"})
    console.print_stdout(f"Using a web browser navigate to: {url}")
    # TODO: use console to get input from the user. https://github.com/pantsbuild/pants/issues/11398
    token_code = input("Type or paste in the token exchange code: ")
    desc = _get_token_desc(options)
    return _exchage_code_for_token(console, options, token_code, description=desc)


def _is_browser_available() -> bool:
    try:
        webbrowser.get()
    except webbrowser.Error:
        return False
    return True


def _get_error_message(response) -> str:
    error_message = None
    request_id = response.headers.get(REQUEST_ID_HEADER, "NA")
    if response.headers.get("Content-Type") == "application/json":
        error_message = response.json().get("message")

    if not error_message:
        error_message = f"Unknown error: {response.text}"
    return f"HTTP: {response.status_code}: {error_message} request={request_id}"


def get_auth_rules():
    return collect_rules()


def _get_token_desc(options: AccessTokenAcquisitionOptions) -> str:
    if options.description:
        return options.description
    default_desc = socket.gethostname()
    if options.log_only:
        default_desc += " [for CI]"
    # TODO: use console to get input from the user. https://github.com/pantsbuild/pants/issues/11398
    user_desc = input(f"Enter token description [{default_desc}]: ")
    return user_desc or default_desc
