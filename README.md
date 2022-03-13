# EQGEN-PY
_For use with [EqualizerAPO](https://sourceforge.net/projects/equalizerapo/)._

## Summary

Generates an EqualizerAPO Graphic EQ preset from 32-bit floating point 
raw audio files of [pink noise](https://en.wikipedia.org/wiki/Pink_noise). 

For use in WSL2, simply run `python3 process.py file.raw | clip.exe` to copy a preset to your clipboard.

## How it Works

Power spectral density is computed over overlapping segments of the signal using SciPy's [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html) function.

The spectral density is normalized based on the mean of its pointwise ratio to the expected 1/f curve, and then the relative spectral power is converted to [power decibels](https://en.wikipedia.org/wiki/Decibel#Power_quantities).

The resulting curve is then [a-weighted](https://en.wikipedia.org/wiki/A-weighting) and its volume loudness normalized.