from scipy import interpolate
import numpy as np
import math

def a_weight(f):
    return 1.2588966 * 148840000 * f**4 / ((f**2 + 424.36) * math.sqrt((f**2 + 11599.29) * (f**2 + 544496.41)) * (f**2 + 148840000))

def to_dB(x):   return 10.0 * math.log10(x)
def from_dB(x): return 10.0 ** (x / 10.0)
vto_dB = np.vectorize(to_dB)
vfrom_dB = np.vectorize(from_dB)

# format: "GraphicEQ: [%f %f;]*"
def parse_eq(eq):
    return np.array(list(map(lambda x: list(map(float, x.strip().split(" "))), eq[11:].split(";"))))
def serialize_eq(points):
    return "GraphicEQ: " + "; ".join(map(lambda x: " ".join(map(lambda x: str(round(x, 4)), x)), points))

def normalize_eq(inpoints):
    points = np.array(inpoints)
    # apply equal-loudness curve
    points[:, 1] *= np.vectorize(a_weight)(points[:, 0])

    total = 0
    totalfac = 0
    for i in range(1, len(points)):
        [fa, ga], [fb, gb] = points[i - 1], points[i]
        fac = 0.5 * (fb - fa) * (a_weight(fa) + a_weight(fb))
        a, b = from_dB(ga), from_dB(gb)

        total += 0.5 * (a + b) * fac
        totalfac += fac
    points[:, 1] = vto_dB(vfrom_dB(points[:, 1]) / (total / totalfac))

    return points

# convert into 'num' equally spaced frequency bins from 20Hz to 20kHz
def clean_interval(points, num=32):
    f = interpolate.interp1d(points[:, 0], points[:, 1], kind="cubic", axis=0)
    return np.array([[x, f(x)] for x in np.linspace(start=20, stop=20_000, num=num)])