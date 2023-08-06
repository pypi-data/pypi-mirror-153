#
#  Copyright ©2022. Levo.ai Inc. All Rights Reserved.
#  You may not copy, reproduce, distribute, publish, display, perform, modify, create derivative works, transmit,
#  or in any way exploit any such software/code, nor may you distribute any part of this software/code over any network,
#  including a local area network, sell or offer it for commercial purposes.
#

from enum import Enum


class ParamType(str, Enum):
    """Resulting status of some action."""

    body = "body"
    query = "query"
    params = "params"
    cookies = "cookies"
    headers = "headers"

    def __str__(self) -> str:
        return self.value
