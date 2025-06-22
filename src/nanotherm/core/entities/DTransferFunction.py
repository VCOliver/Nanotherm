#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

from dataclasses import dataclass
import control as ctrl
from nanotherm.core.domain.transferFunction import ITransferFunction

@dataclass(frozen=True)
class DiscreteTransferFunction(ITransferFunction):
    """
    Discrete transfer function with a specified sampling time.

    Attributes:
        num (list or array): Numerator coefficients of the transfer function.
        den (list or array): Denominator coefficients of the transfer function.
        Ts (float): Sampling time of the discrete system.
    """
    num: list
    den: list
    Ts: float

    @property
    def tf(self):
        return ctrl.TransferFunction(self.num, self.den, self.Ts)