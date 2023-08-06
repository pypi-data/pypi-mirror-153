#
#  Copyright ©2022. Levo.ai Inc. All Rights Reserved.
#  You may not copy, reproduce, distribute, publish, display, perform, modify, create derivative works, transmit,
#  or in any way exploit any such software/code, nor may you distribute any part of this software/code over any network,
#  including a local area network, sell or offer it for commercial purposes.
#

from __future__ import annotations

from enum import Enum


class Status(str, Enum):
    """Resulting status of some action."""

    success = "success"
    failure = "failure"
    error = "error"
    skipped = "skipped"

    def __str__(self) -> str:
        return self.value

    def __add__(self, other: str) -> str:
        """Error > Failure > Success > Skipped."""
        if self == Status.error or other == Status.error:
            return Status.error

        if self == Status.failure or other == Status.failure:
            return Status.failure

        if self == Status.skipped:
            return other

        return Status.success if other == Status.success else other + self
