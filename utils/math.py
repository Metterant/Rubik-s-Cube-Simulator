import math

def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

def smoothstep(t: float) -> float:
    t = clamp(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)

def lerp(start, end, t):
    t = smoothstep(t)
    return start * (1 - t) + end * t