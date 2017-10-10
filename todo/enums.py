"""Enums are defined here"""
from enum import Enum, auto


class Status(Enum):
    """Enum for Task status"""
    TO_DO = auto()
    IN_PROGRESS = auto()
    DONE = auto()
