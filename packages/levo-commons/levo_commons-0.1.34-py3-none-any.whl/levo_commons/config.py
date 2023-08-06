#
#  Copyright ©2022. Levo.ai Inc. All Rights Reserved.
#  You may not copy, reproduce, distribute, publish, display, perform, modify, create derivative works, transmit,
#  or in any way exploit any such software/code, nor may you distribute any part of this software/code over any network,
#  including a local area network, sell or offer it for commercial purposes.
#

from logging import Handler
from typing import Dict, Optional, Tuple

import attr

from .models import Module
from .providers import Provider

CONFIG_VERSION = (1, 0)
DEFAULT_REQUEST_TIMEOUT = 30


@attr.s(slots=True)
class AuthConfig:
    auth_type: str = attr.ib(kw_only=True, default="None")
    username: Optional[str] = attr.ib(kw_only=True, default=None)
    password: Optional[str] = attr.ib(kw_only=True, default=None)
    api_key: Optional[str] = attr.ib(kw_only=True, default=None)
    token: Optional[str] = attr.ib(kw_only=True, default=None)


@attr.s(slots=True, kw_only=True)
class PlanConfig:
    """Test plan configuration."""

    # Current config version
    version = CONFIG_VERSION

    target_url: str = attr.ib(kw_only=True)
    spec_path: Optional[str] = attr.ib(kw_only=True, default=None)
    test_plan_path: Optional[str] = attr.ib(kw_only=True, default=None)
    # This is deprecated and should be removed in next version.
    auth: Optional[Tuple[str, str]] = attr.ib(kw_only=True, default=None)
    auth_type: Optional[str] = attr.ib(kw_only=True, default=None)
    report_to_saas: bool = attr.ib(kw_only=True, default=True)
    auth_config: Optional[AuthConfig] = attr.ib(kw_only=True, default=None)
    headers: Dict[str, str] = attr.ib(kw_only=True, factory=dict)
    env_file_path: Optional[str] = attr.ib(kw_only=True, default=None)
    ignore_ssl_verify: bool = attr.ib(kw_only=True, default=False)
    suite_execution_delay: int = attr.ib(kw_only=True, default=0)
    request_timeout: int = attr.ib(kw_only=True, default=DEFAULT_REQUEST_TIMEOUT)

    # Module providers
    module_providers: Dict[Module, Provider] = attr.ib(kw_only=True, factory=dict)

    # Log handlers
    test_case_log_handler: Optional[Handler] = attr.ib(kw_only=True, default=None)
    runner_log_handler: Optional[Handler] = attr.ib(kw_only=True, default=None)

    # Shortcut to convert PlanConfig to dictionary
    asdict = attr.asdict
