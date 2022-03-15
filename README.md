# EQGEN-PY
_For use with [EqualizerAPO](https://sourceforge.net/projects/equalizerapo/)._

## Summary

Generates an EqualizerAPO Graphic EQ preset from 32-bit floating point raw audio files of [pink noise](https://en.wikipedia.org/wiki/Pink_noise) to adjust output frequency response, such that it closely approximates the [a-weighing curve](https://en.wikipedia.org/wiki/A-weighting). Removing the a-weighting can approximate a flat response, although this is not ideal for music.

For use in WSL2, simply run `python3 process.py file.raw | clip.exe` to copy a preset to your clipboard.

## How it Works

Power spectral density is computed over overlapping segments of the signal using SciPy's [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html) function.

The measured spectral density is normalized to fit a target 1/f curve. Then, the target density is divided by the measured power density pointwise at each measured frequency, and the the ratios are converted to [power decibels](https://en.wikipedia.org/wiki/Decibel#Power_quantities). The resulting decibels represent an approximate gain to apply to each frequency band to flatten the response on output.

The resulting curve is then [a-weighted](https://en.wikipedia.org/wiki/A-weighting).