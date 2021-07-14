from dataclasses import dataclass, field

from .point import Point


# TODO: maybe use better name instead of the generic-sounding `Point`.
@dataclass
class Note:
    """Note docstring."""
    points: list[Point] = field(default_factory=list)
    