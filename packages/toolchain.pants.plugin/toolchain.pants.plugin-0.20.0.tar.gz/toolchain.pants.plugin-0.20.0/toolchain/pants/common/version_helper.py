# Copyright © 2022 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from __future__ import annotations

from pants.version import VERSION as PANTS_VERSION

_PANTS_MINOR_VERSION = int(PANTS_VERSION.split(".")[1])


def use_new_options() -> bool:
    return _PANTS_MINOR_VERSION >= 11


def use_git_work_tree_rule() -> bool:
    return _PANTS_MINOR_VERSION >= 12
