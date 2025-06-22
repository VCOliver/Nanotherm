#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class ITransferFunction:
    """
    Abstract representation of a transfer function.

    Attributes:
        num (Sequence[float]): Numerator coefficients of the transfer function.
        den (Sequence[float]): Denominator coefficients of the transfer function.
    """
    num: Sequence[float]
    den: Sequence[float]

