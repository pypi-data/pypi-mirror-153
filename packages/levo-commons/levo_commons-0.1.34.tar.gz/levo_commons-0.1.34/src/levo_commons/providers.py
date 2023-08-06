#
#  Copyright ©2022. Levo.ai Inc. All Rights Reserved.
#  You may not copy, reproduce, distribute, publish, display, perform, modify, create derivative works, transmit,
#  or in any way exploit any such software/code, nor may you distribute any part of this software/code over any network,
#  including a local area network, sell or offer it for commercial purposes.
#

import subprocess
from abc import ABC, abstractmethod
from pathlib import Path


class Provider(ABC):
    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError("Provider should implement a start method.")

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError("Provider should implement a stop method.")

    @abstractmethod
    def is_running(self) -> bool:
        raise NotImplementedError("Provider should implement an is_running method.")


class ZaproxyProvider(Provider, ABC):
    """Provides information about a running ZAP instance."""

    @property
    @abstractmethod
    def ip(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def port(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def home_directory(self) -> Path:
        raise NotImplementedError

    @property
    @abstractmethod
    def api_key(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def process(self) -> subprocess.Popen[bytes]:
        raise NotImplementedError
