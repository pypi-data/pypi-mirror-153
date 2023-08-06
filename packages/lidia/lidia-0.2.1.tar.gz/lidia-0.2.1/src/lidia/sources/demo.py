from argparse import _SubParsersAction, ArgumentDefaultsHelpFormatter, ArgumentError, ArgumentParser, Namespace
from math import pi, sin
from multiprocessing import Queue
from time import sleep, time
from typing import Tuple

from ..types import AircraftState, Buttons, Controls, RunFn


def setup(subparsers: _SubParsersAction) -> Tuple[str, RunFn]:
    NAME = 'demo'
    parser: ArgumentParser = subparsers.add_parser(
        NAME,
        help='looping simulation demonstrating GUI',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--period', '-T', type=float,
                        help='loop time in seconds', default=5.0)
    parser.add_argument('--frequency', '-f', type=float,
                        help='number of messages sent per second', default=30.0)
    parser.add_argument('--no-trim', action='store_false', dest='trim',
                        help='do not demonstrate trim function')
    parser.add_argument('--no-borders', action='store_false', dest='borders',
                        help='do not demonstrate borders function')

    return (NAME, run)


def run(q: Queue, args: Namespace):
    if args.period <= 0:
        raise ArgumentError(args.frequency, 'period must be positive')
    if args.frequency <= 0:
        raise ArgumentError(args.frequency, 'frequency must be positive')

    def val(phase):
        """Generate a sinusoidal value with phase offset (from 0 to 1)"""
        return 0.6 * sin((time() / args.period + phase) * 2 * pi)

    def cycle_index(): return int(time() // args.period) % 3
    def current_phase(): return (time() / args.period) % 1

    last_trim = Controls()

    while True:
        state = AircraftState()

        state.ctrl.stick_pull = val(0.1)
        state.ctrl.stick_right = val(0.35)
        state.ctrl.collective_up = 0.3 + 0.5 * val(0.2)

        state.trgt.stick_pull = val(0.55)
        state.trgt.stick_right = val(0.3)
        state.trgt.collective_up = 0.3 + 0.5 * val(0.4)

        if cycle_index() == 1 and args.trim:
            if current_phase() < 0.4:
                state.btn |= Buttons.COLL_FTR
            if current_phase() > 0.6:
                state.btn |= Buttons.CYC_FTR

        if state.btn & Buttons.COLL_FTR:
            last_trim.collective_up = state.ctrl.collective_up
        if state.btn & Buttons.CYC_FTR:
            last_trim.stick_right = state.ctrl.stick_right
            last_trim.stick_pull = state.ctrl.stick_pull
        state.trim = last_trim

        if cycle_index() == 2 and args.borders:
            if current_phase() < 0.5:
                state.brdr.low = Controls(-0.8, -0.8, 0.1, -0.8, 0.1)
                state.brdr.high = Controls(0.8, 0.8, 0.9, 0.8, 0.9)
            if current_phase() > 0.5:
                state.brdr.low = Controls(-0.5, -0.5, 0.25, -0.5, 0.25)
                state.brdr.high = Controls(0.5, 0.5, 0.75, 0.5, 0.75)

        q.put(('smol', state.smol()))
        sleep(1 / args.frequency)
