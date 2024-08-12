import os
from types import FrameType

from crosscutting.strings import STOPPED


def handle_sigint(signal: int, frame: FrameType) -> None:
    print(f"\r{STOPPED}")
    exit(0)


def clear_screen() -> None:
    if 'nt' in os.name:
        os.system('cls')
    elif 'posix' in os.name:
        os.system('clear')
