"""
tracks.sleep_features — module 3 additions for the Sleep-EDF track (iteration 3).

Each feature GROUP is one function `rec -> (names, matrix)` with one row per
30-s epoch, so groups can be switched on one at a time from the config
(`cfg["feature_groups"]`) and compared under the same harness. Two further
steps act on the whole feature matrix of ONE night: `night_norm` and `context`.

Nothing here learns from labels or from another recording: every statistic
(a threshold, a median, a percentile) comes from the one night in front of it,
so building features before `evaluate()` cuts the folds stays leakage-safe.
"""
from __future__ import annotations
import numpy as np
from scipy.signal import welch, butter, sosfiltfilt, hilbert

BANDS = {"delta": (0.5, 4), "theta": (4, 8), "alpha": (8, 11),
         "sigma": (11, 16), "beta": (16, 30)}          # same edges as bsp.sleep_pipeline
TOTAL = (0.5, 30)

ADDITIVE_GROUPS = ("relpow", "spindle", "eogemg", "pz")
MATRIX_STEPS = ("night_norm", "context")               # applied in this order, after the groups
ALL_GROUPS = ADDITIVE_GROUPS + MATRIX_STEPS

_EPS = 1e-20


def _psd(x, fs, nperseg=256):
    """Welch PSD of every epoch at once (rows = epochs)."""
    return welch(x, fs=fs, nperseg=min(nperseg, x.shape[-1]), axis=-1)


def _band(f, P, lo, hi):
    m = (f >= lo) & (f < hi)
    return np.trapezoid(P[:, m], f[m], axis=-1)


# --------------------------------------------------------------- groups
def relpow(rec, channel="eeg"):
    """Relative band powers + log total power + log band ratios."""
    f, P = _psd(rec.epochs[channel], rec.fs)
    bp = {b: _band(f, P, *e) for b, e in BANDS.items()}
    tot = _band(f, P, *TOTAL) + _EPS
    cols = {f"rel_{b}": v / tot for b, v in bp.items()}
    cols["log_total"] = np.log(tot)
    cols["log_delta_theta"] = np.log((bp["delta"] + _EPS) / (bp["theta"] + _EPS))
    cols["log_theta_alpha"] = np.log((bp["theta"] + _EPS) / (bp["alpha"] + _EPS))
    cols["log_alpha_beta"] = np.log((bp["alpha"] + _EPS) / (bp["beta"] + _EPS))
    return list(cols), np.column_stack(list(cols.values()))


def spindle(rec, band=(11.0, 16.0), k=2.5, dur=(0.5, 2.0)):
    """Sigma-band spindle detector (band-pass -> Hilbert envelope -> threshold
    -> duration rule) plus the sigma peak prominence of the PSD."""
    eeg, fs = rec.epochs["eeg"], rec.fs
    sos = butter(4, band, btype="band", fs=fs, output="sos")
    env = np.abs(hilbert(sosfiltfilt(sos, eeg, axis=-1), axis=-1))
    night_med = np.median(env) + _EPS                  # this night only
    above = env > k * night_med
    lo, hi = int(dur[0] * fs), int(dur[1] * fs)
    count = np.zeros(len(eeg))
    for i, row in enumerate(above):
        d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
        lengths = np.flatnonzero(d == -1) - np.flatnonzero(d == 1)
        count[i] = np.sum((lengths >= lo) & (lengths <= hi))
    f, P = _psd(eeg, fs, nperseg=512)
    sig = P[:, (f >= band[0]) & (f <= band[1])].max(axis=1)
    flank = P[:, ((f >= 8) & (f < 10)) | ((f > 17) & (f <= 20))].mean(axis=1)
    cols = {"spindle_count": count,
            "spindle_env_max": env.max(axis=1) / night_med,
            "sigma_prominence": np.log((sig + _EPS) / (flank + _EPS))}
    return list(cols), np.column_stack(list(cols.values()))


def eogemg(rec, k=4.0):
    """EOG slow / rapid eye-movement power and deflection count; chin-EMG tone.

    Sleep-Cassette stores `EMG submental` at 1 Hz (an amplitude envelope), so
    only level-type EMG features are meaningful, not spectral ones."""
    eog, emg, fs = rec.epochs["eog"], rec.epochs["emg"], rec.fs
    f, P = _psd(eog, fs, nperseg=1000)                 # 0.1 Hz resolution for the slow band
    sem = _band(f, P, 0.3, 1.0)
    rem = _band(f, P, 1.0, 5.0)
    sos = butter(4, (0.5, 5.0), btype="band", fs=fs, output="sos")
    eog_f = sosfiltfilt(sos, eog, axis=-1)
    thr = k * np.median(np.abs(eog_f))                 # this night only
    crossings = np.diff((np.abs(eog_f) > thr).astype(np.int8), axis=-1) == 1
    level = np.abs(emg).mean(axis=1)
    p10 = np.percentile(level, 10) + _EPS              # this night's own floor
    cols = {"eog_log_sem": np.log(sem + _EPS),
            "eog_log_rem": np.log(rem + _EPS),
            "eog_deflections": crossings.sum(axis=1).astype(float),
            "emg_log_level": np.log(level + _EPS),
            "emg_rel_night": np.log(level / p10 + _EPS),
            "emg_log_std": np.log(emg.std(axis=1) + _EPS)}
    return list(cols), np.column_stack(list(cols.values()))


def pz(rec):
    """The 5 absolute band powers + spectral entropy from EEG Pz-Oz."""
    if "eeg2" not in rec.epochs:
        raise KeyError("feature group 'pz' needs the Pz-Oz channel (epochs['eeg2']); "
                       "reload with the current SleepEDFTrack.load().")
    f, P = _psd(rec.epochs["eeg2"], rec.fs)
    cols = {f"pz_{b}": _band(f, P, *e) for b, e in BANDS.items()}
    m = (f >= TOTAL[0]) & (f <= TOTAL[1])
    p = P[:, m] / (P[:, m].sum(axis=1, keepdims=True) + _EPS)
    cols["pz_spec_entropy"] = -(p * np.log(p + _EPS)).sum(axis=1) / np.log(m.sum())
    return list(cols), np.column_stack(list(cols.values()))


GROUP_FUNCS = {"relpow": relpow, "spindle": spindle, "eogemg": eogemg, "pz": pz}


# ------------------------------------------------- whole-night matrix steps
def night_norm(names, X):
    """Robust z-score of every column within this night (median / IQR)."""
    med = np.median(X, axis=0)
    iqr = np.subtract(*np.percentile(X, [75, 25], axis=0))
    return names, (X - med) / np.where(iqr > 0, iqr, 1.0)


def context(names, X):
    """Append the previous and the next epoch's features (edges repeat)."""
    prev = np.vstack([X[:1], X[:-1]])
    nxt = np.vstack([X[1:], X[-1:]])
    return (names + [f"prev_{n}" for n in names] + [f"next_{n}" for n in names],
            np.hstack([X, prev, nxt]))


def add_feature_groups(rec, names, X, groups):
    """Append the requested groups to one night's base features, then apply the
    whole-night steps in a fixed order (night_norm before context, so the
    neighbours are normalised the same way as the epoch itself)."""
    groups = tuple(groups or ())
    unknown = sorted(set(groups) - set(ALL_GROUPS))
    if unknown:
        raise ValueError(f"unknown feature group(s) {unknown}; choose from {ALL_GROUPS}")
    names = list(names)
    for g in ADDITIVE_GROUPS:
        if g in groups:
            n, M = GROUP_FUNCS[g](rec)
            names += n
            X = np.hstack([X, M])
    if "night_norm" in groups:
        names, X = night_norm(names, X)
    if "context" in groups:
        names, X = context(names, X)
    return names, X
