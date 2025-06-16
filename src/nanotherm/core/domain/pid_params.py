#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

from dataclasses import dataclass

@dataclass(frozen=True)
class PIDParams:
    """
    Holds the proportional, integral, and derivative gains
    for a PID controller.
    """
    kp: float
    ki: float
    kd: float
    
    def __str__(self) -> str:
        """Return a user-friendly string representation of PID parameters."""
        return f"PID(Kp={self.kp}, Ki={self.ki}, Kd={self.kd})"
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f"PIDParams(kp={self.kp}, ki={self.ki}, kd={self.kd})"