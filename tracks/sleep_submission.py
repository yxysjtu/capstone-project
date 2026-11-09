"""
tracks.sleep_submission — module 6 (inference) for nights cropped to the lights-off window.

The instructor scores `predictions.csv` with `score_submission()` against the FULL
hold-out nights (every epoch `load()` returns), and raises on any missing row. The
model, however, is trained and applied only inside the lights-off window
(`sleep_crop.crop_lights_off`). So the window's predictions have to be put back at
their full-night positions, and the epochs outside the window need a label too.

Outside the window is filled with Wake: the window runs from 30 min before
lights-off to 9.5 h after it, and on the 10 training subjects it holds at least
98.4 % of each night's sleep. The scored κ then includes those (mostly easy) Wake
epochs, so it is NOT comparable to the cross-validated κ computed inside the window.
"""
from __future__ import annotations
import csv

import numpy as np

from sleep_crop import crop_lights_off, EPOCH_S


def window_start(rec, off, margin_min=30):
    """First epoch of the lights-off window (the same rule as `crop_lights_off`)."""
    return max(off[rec.meta["record"]] - int(margin_min * 60 / EPOCH_S), 0)


def predict_full_night(track, rec, off, model, fill="W", hours=9, margin_min=30):
    """One label per epoch of the FULL night: the frozen model's predictions inside the
    lights-off window, `fill` outside it."""
    n = len(next(iter(rec.epochs.values())))
    start = window_start(rec, off, margin_min)
    pred = track.infer(model, crop_lights_off(rec, off, hours=hours, margin_min=margin_min))
    full = np.full(n, fill, dtype=object)
    full[start:start + len(pred)] = pred
    return full


def write_full_night_submission(track, full_recs, off, path, model, fill="W", hours=9, margin_min=30):
    """Write `predictions.csv` (`record,epoch,label`) with one row per epoch of each full
    night, so `score_submission()` finds every key. `full_recs` are uncropped nights,
    as `download_holdout()` + `load()` give them; `off` is `lights_off_epochs(full_recs, ...)`."""
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["record", "epoch", "label"])
        for rec in full_recs:
            full = predict_full_night(track, rec, off, model, fill, hours, margin_min)
            for i, p in enumerate(full):
                w.writerow([rec.meta["record"], i, p])
    return path
