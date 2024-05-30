import os
from types import FrameType


def handle_sigint(signal: int, frame: FrameType) -> None:
    print('\rStopped')
    exit(0)


def clear_screen() -> None:
    if 'nt' in os.name:
        os.system('cls')
    elif 'posix' in os.name:
        os.system('clear')
