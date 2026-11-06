import csv
import glob
import os

import numpy as np
from adapter import Recording

EPOCH_S = 30                            
SUBJECTS_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SC-subjects.csv")


# Old crop (uses labels)
def crop_to_sleep(rec, margin_min=30):
    """Crop one night to the sleep period +/- margin_min minutes.
    Uses the labels, so it is only valid on training nights.
    Kept unchanged so that RESULTS.md rows 2.2-3.7 can still be reproduced."""
    labels = np.asarray(rec.labels)

    # 1. indices of all epochs that are NOT "W"
    sleep_idx = np.flatnonzero(labels != "W")
    if len(sleep_idx) == 0:          # no sleep in this night -> leave it unchanged
        return rec

    # 2. first and last sleep epoch
    first = sleep_idx[0]
    last = sleep_idx[-1]
    
    # 3. how many epochs is margin_min minutes?
    margin = int(margin_min * 60 / EPOCH_S)

    # 4. start and stop, without going outside the recording
    start = max(first - margin, 0)
    stop = min(last + margin + 1, len(labels))

    # 5. new Recording containing only that segment
    return Recording(group=rec.group, fs=rec.fs,
                     epochs={k: v[start:stop] for k, v in rec.epochs.items()},
                     labels=labels[start:stop], meta=rec.meta)


# New crop (uses lights-off)
def read_subjects(csv_path=SUBJECTS_CSV):
    """SC-subjects.csv (exported from PhysioNet SC-subjects.xls) -> {(subject, night): row}."""
    table = {}
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            table[(int(row["subject"]), int(row["night"]))] = row
    return table


def subject_night(rec):
    """'SC4001E0' -> (0, 1): characters 3-4 are the subject, character 5 the night."""
    record = rec.meta["record"]
    return int(record[3:5]), int(record[5])


def lights_off_epochs(recs, cache_dir, csv_path=SUBJECTS_CSV):
    """Epoch index of lights-off for every night -> {"SC4001E0": 1010, ...}.
    Uses only the clock: lights-off from SC-subjects.csv and the recording
    start time from the EDF header. No labels -> works for test nights too.
    Assumption: epoch k starts k * 30 s after the recording starts."""
    import mne
    table = read_subjects(csv_path)

    off = {}
    for rec in recs:
        record = rec.meta["record"]
        key = subject_night(rec)
        if key not in table:
            raise KeyError(f"{record}: subject {key[0]}, night {key[1]} is missing in {csv_path}")

        # 1. recording start (clock time) from the EDF header
        psg = glob.glob(os.path.join(cache_dir, "**", record + "-PSG.edf"), recursive=True)[0]
        start = mne.io.read_raw_edf(psg, preload=False, verbose="ERROR").info["meas_date"]
        start_s = start.hour * 3600 + start.minute * 60 + start.second

        # 2. lights-off (clock time) in seconds after midnight
        h, m = table[key]["LightsOff"].strip().split(":")[:2]
        off_s = int(h) * 3600 + int(m) * 60

        # 3. seconds from recording start to lights-off
        seconds = off_s - start_s
        if seconds < 0:          # lights-off after midnight (e.g. 0:38), start was the afternoon before
            seconds += 24 * 3600
        off[record] = int(seconds // EPOCH_S)
    return off


def crop_lights_off(rec, off, hours=9, margin_min=30):
    """Crop one night to [lights-off - margin_min, lights-off + hours + margin_min].
    Fixed window, chosen without labels -> the same rule on training and test nights.
    hours=9: upper end of the recommended 7-9 h,
    fixed before running and not tuned on our data.
    Labels are cut along so they stay aligned."""
    n = len(next(iter(rec.epochs.values())))
    lo = off[rec.meta["record"]]
    margin = int(margin_min * 60 / EPOCH_S)
    start = max(lo - margin, 0)
    stop = min(lo + int(hours * 3600 / EPOCH_S) + margin, n)
    labels = None if rec.labels is None else np.asarray(rec.labels)[start:stop]
    return Recording(group=rec.group, fs=rec.fs,
                     epochs={k: v[start:stop] for k, v in rec.epochs.items()},
                     labels=labels, meta=rec.meta)


def stage_counts(recs):
    """Number (and %) of epochs per sleep stage, across all nights."""
    all_labels = np.concatenate([np.asarray(r.labels) for r in recs])
    stages, counts = np.unique(all_labels, return_counts=True)
    return {s: f"{n} ({100 * n / len(all_labels):.0f} %)" for s, n in zip(stages, counts)}