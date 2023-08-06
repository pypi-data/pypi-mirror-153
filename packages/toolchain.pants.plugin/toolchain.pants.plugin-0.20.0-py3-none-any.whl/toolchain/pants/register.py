# Copyright © 2019 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from toolchain.pants.auth.rules import get_auth_rules
from toolchain.pants.common.toolchain_setup import get_rules as common_rules
from toolchain.pants.common.version_helper import use_git_work_tree_rule

if use_git_work_tree_rule():
    from toolchain.pants.buildsense.rules_new_pants import rules_buildsense_reporter
else:
    from toolchain.pants.buildsense.rules_old_pants import rules_old_pants as rules_buildsense_reporter


def rules():
    return (
        *common_rules(),
        *get_auth_rules(),
        *rules_buildsense_reporter(),
    )
