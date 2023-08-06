# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

Artifacts = Dict[str, bytes]
WorkUnits = List[dict]
WorkUnitsMap = Dict[str, dict]


@dataclass
class RunTrackerBuildInfo:
    has_ended: bool
    build_stats: dict
    log_file: Path | None

    @property
    def run_id(self) -> str:
        return self.build_stats["run_info"]["id"]
