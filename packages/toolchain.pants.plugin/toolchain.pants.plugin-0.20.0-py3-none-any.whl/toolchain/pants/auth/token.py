# Copyright © 2021 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from __future__ import annotations

import base64
import datetime
import json
from dataclasses import asdict, dataclass
from typing import cast

from toolchain.base.datetime_tools import utcnow


@dataclass(frozen=True)
class AuthToken:
    access_token: str
    expires_at: datetime.datetime
    user: str | None = None
    repo: str | None = None
    repo_id: str | None = None
    customer_id: str | None = None

    @classmethod
    def no_token(cls) -> AuthToken:
        return cls(access_token="", expires_at=datetime.datetime(2020, 1, 1))  # nosec

    @classmethod
    def from_json_dict(cls, json_dict: dict):
        return cls(
            access_token=json_dict["access_token"],
            expires_at=datetime.datetime.fromisoformat(json_dict["expires_at"]),
            user=json_dict.get("user"),
            repo=json_dict.get("repo"),
            repo_id=json_dict.get("repo_id"),
            customer_id=json_dict.get("customer_id"),
        )

    @classmethod
    def from_access_token_string(cls, token_str: str) -> AuthToken:
        claims_segment = token_str.split(".")[1].encode()
        claims = json.loads(base64url_decode(claims_segment))
        expires_at = datetime.datetime.utcfromtimestamp(claims["exp"]).replace(tzinfo=datetime.timezone.utc)
        return cls(
            access_token=token_str, expires_at=expires_at, user=claims["toolchain_user"], repo=claims["toolchain_repo"]
        )

    def get_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.access_token}"}

    def has_expired(self) -> bool:
        expiration_time = cast(datetime.datetime, self.expires_at) - datetime.timedelta(
            seconds=10
        )  # Give some room for clock deviation and processing time.
        return utcnow() > expiration_time

    @property
    def has_token(self) -> bool:
        return bool(self.access_token)

    def to_json_string(self) -> str:
        token_dict = asdict(self)
        token_dict["expires_at"] = self.expires_at.isoformat()
        return json.dumps(token_dict)


def base64url_decode(data: bytes) -> bytes:
    # based on jose/utils.py
    rem = len(data) % 4
    if rem > 0:
        data += b"=" * (4 - rem)
    return base64.urlsafe_b64decode(data)
