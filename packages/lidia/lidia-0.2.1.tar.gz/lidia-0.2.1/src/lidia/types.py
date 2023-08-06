from argparse import _SubParsersAction, Namespace
from dataclasses import dataclass
from enum import IntFlag
from multiprocessing import Queue
from typing import Callable, List, NoReturn, Tuple


RunFn = Callable[[Queue, Namespace], NoReturn]
SetupFn = Callable[[_SubParsersAction], Tuple[str, RunFn]]


@dataclass
class Controls:
    stick_right: float = 0
    stick_pull: float = 0
    throttle: float = 0
    pedals_right: float = 0
    collective_up: float = 0

    def smol(self) -> List[float]:
        return [
            self.stick_right,
            self.stick_pull,
            self.throttle,
            self.pedals_right,
            self.collective_up
        ]


class Borders:
    def __init__(self) -> None:
        self.low = Controls(-1, -1, 0, -1, 0)
        self.high = Controls(1, 1, 1, 1, 1)

    def smol(self) -> dict:
        return {
            'low': self.low.smol(),
            'high': self.high.smol()
        }


class Buttons(IntFlag):
    NONE = 0
    CYC_FTR = 1 << 0
    COLL_FTR = 1 << 1

    def smol(self) -> List[int]:
        return [int(self)]


class AircraftState:
    """Full state of displayed aircraft initialised with defaults"""

    def __init__(self) -> None:
        self.ctrl = Controls()
        """Current control inceptors position"""
        self.trgt = Controls()
        """Target inceptors position"""
        self.trim = Controls()
        """Controls trim"""
        self.brdr = Borders()
        """Task borders for inceptors"""
        self.btn = Buttons.NONE
        """Currently pressed buttons"""

    def smol(self) -> dict:
        """Return self as dictionary with SMOL-defined keys"""
        d = dict()
        for key in ['ctrl', 'trgt', 'trim', 'brdr', 'btn']:
            d[key] = getattr(self, key).smol()
        return d
