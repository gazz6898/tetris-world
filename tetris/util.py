from typing import Any, List, Tuple

class PieceOutOfBoundsException(Exception):
    pass

def sign(x: int):
    return -1 if x < 0 else 1


def has_index(xs: List[Any], i: int):
    return i >= 0 and i < len(xs)

# Yes, this is just a glorified identity function.
def rot0(coords: Tuple[float, float]):
    (x, y) = coords
    return (x, y)

def rot90(coords: Tuple[float, float]):
    (x, y) = coords
    return (y, -x)


def rot180(coords: Tuple[float, float]):
    (x, y) = coords
    return (-x, -y)


def rot270(coords: Tuple[float, float]):
    (x, y) = coords
    return (-y, x)
