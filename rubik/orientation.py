from __future__ import annotations
from math import cos, sin, pi
from dataclasses import dataclass

Matrix3 = tuple[
    tuple[int, int, int],
    tuple[int, int, int],
    tuple[int, int, int],
]

@dataclass(frozen=True)
class Orientation:
    matrix: Matrix3 = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
    )

    def __mul__(self, other: Orientation | tuple[int, int, int]):
        if isinstance(other, Orientation):
            result: Matrix3 = tuple(
                tuple(
                    sum(self.matrix[row][k] * other.matrix[k][column] for k in range(3))
                    for column in range(3)
                )
                for row in range(3)
            )  # type: ignore[assignment]
            return Orientation(result)

        if isinstance(other, tuple) and len(other) == 3:
            return tuple(
                sum(self.matrix[row][k] * other[k] for k in range(3))
                for row in range(3)
            )

        return NotImplemented
    
    @classmethod
    def identity(cls) -> Orientation:
        return cls()
    
    @classmethod
    def rotated_x(cls, degrees) -> Orientation:
        theta = degrees * pi / 180
        m = (
            (1, 0, 0),
            (0, round(cos(theta)), round(-sin(theta))),
            (0, round(sin(theta)), round(cos(theta))),
        )
        return Orientation(m)
    
    @classmethod
    def rotated_y(cls, degrees) -> Orientation:
        theta = degrees * pi / 180
        m = (
            (round(cos(theta)), 0, round(sin(theta))),
            (0, 1, 0),
            (round(-sin(theta)), 0, round(cos(theta))),
        )
        return Orientation(m)
    
    @classmethod
    def rotated_z(cls, degrees) -> Orientation:
        theta = degrees * pi / 180
        m = (
            (round(cos(theta)), round(-sin(theta)), 0),
            (round(sin(theta)), round(cos(theta)), 0),
            (0, 0, 1),
        )
        return Orientation(m)