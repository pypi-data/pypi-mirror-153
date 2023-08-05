from math import ceil
from typing import Optional

import neurokit2 as nk
import numpy as np

from .interface import BaseOscillationInterface
from ..utils.types import BaseOscillationKind


class ECG(BaseOscillationInterface):
    def get_timeseries_periods(self) -> Optional[int]:
        return int((self.length / 100) * self.frequency)

    def get_base_oscillation_kind(self) -> BaseOscillationKind:
        return BaseOscillationKind.ECG

    def generate_only_base(self,
                           length: Optional[int] = None,
                           frequency: Optional[float] = None,
                           channels: Optional[int] = None,
                           *args, **kwargs) -> np.ndarray:
        length = length or self.length
        frequency = int(frequency or self.frequency)

        periods = (length / 100) * frequency
        sampling_rate = ceil(length / 10.0)
        ecg = nk.ecg_simulate(duration=10,
                              sampling_rate=sampling_rate,
                              heart_rate=periods * 6,
                              random_state=np.random.get_state()[1][0],  # type: ignore
                              method='simple')[:length]
        return ecg
