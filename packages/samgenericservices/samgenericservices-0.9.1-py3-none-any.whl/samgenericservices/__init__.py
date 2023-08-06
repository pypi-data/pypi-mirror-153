# coding=utf-8
"""
samgenericservices
"""

__version__ = "0.9.1"

from typing import Tuple

from .BaseMicroService import (BaseMicroService as BaseMicroService)
from .FAAPIService import (FAAPIService as FAAPIService)
from .IQNFCService import (IQNFCService as IQNFCService)


__all__: Tuple[str, ...] = (
        "BaseMicroService",
        "FAAPIService",
        "IQNFCService",
        )
