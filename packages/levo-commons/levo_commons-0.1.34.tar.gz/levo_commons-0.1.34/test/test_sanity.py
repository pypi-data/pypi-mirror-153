#
#  Copyright ©2022. Levo.ai Inc. All Rights Reserved.
#  You may not copy, reproduce, distribute, publish, display, perform, modify, create derivative works, transmit,
#  or in any way exploit any such software/code, nor may you distribute any part of this software/code over any network,
#  including a local area network, sell or offer it for commercial purposes.
#

import attr
import pytest

from levo_commons.events import Finished, Payload


@attr.s(slots=True)
class ExamplePayload(Payload):
    foo: int = attr.ib()


def test_events_api():
    event = Finished(running_time=1.0, payload=ExamplePayload(foo=42))
    assert event.running_time == pytest.approx(1.0)
    assert event.asdict() == {
        "payload": {"foo": 42},
        "running_time": pytest.approx(1.0),
    }
