from util import to_dB, serialize_eq, normalize_eq, clean_interval
import numpy as np
from scipy import signal
import struct
import sys

SAMPLE_RATE = 44100
OUT_BANDS   = 128

with open(sys.argv[1], "rb") as f: 
    data = f.read()
    samples = struct.unpack("f"*(len(data)//4), data)

sigdens = signal.welch(samples, fs=SAMPLE_RATE, nperseg=4096)
sigdens = np.stack((sigdens[0], sigdens[1]), axis=1)[1:]
# normalize spectral density curve to expected
sigdens[:, 1] /= np.mean(sigdens[1:, 1] * sigdens[1:, 0])

ineq = np.stack((sigdens[:, 0], np.vectorize(to_dB)(sigdens[:, 0] * sigdens[:, 1])), axis=1)
outeq = clean_interval(normalize_eq(ineq), num=OUT_BANDS)
print(serialize_eq(outeq))