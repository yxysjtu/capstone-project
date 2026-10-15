import numpy as np
from adapter import Recording


def crop_to_sleep(rec, margin_min=30):
    """Crop one night to the sleep period +/- margin_min minutes."""
    labels = np.asarray(rec.labels)

    # 1. indices of all epochs that are NOT "W"
    sleep_idx = np.flatnonzero(labels != "W")
    if len(sleep_idx) == 0:          # no sleep in this night -> leave it unchanged
        return rec

    # 2. first and last sleep epoch
    first = sleep_idx[0]
    last = sleep_idx[-1]

    # 3. how many epochs is margin_min minutes? (one epoch = 30 s)
    margin = int(margin_min * 60 / 30)

    # 4. start and stop, without going outside the recording
    start = max(first - margin, 0)
    stop = min(last + margin + 1, len(labels))

    # 5. new Recording containing only that segment
    return Recording(group=rec.group, fs=rec.fs,
                     epochs={k: v[start:stop] for k, v in rec.epochs.items()},
                     labels=labels[start:stop], meta=rec.meta)


def stage_counts(recs):
    """Number (and %) of epochs per sleep stage, across all nights."""
    all_labels = np.concatenate([np.asarray(r.labels) for r in recs])
    stages, counts = np.unique(all_labels, return_counts=True)
    return {s: f"{n} ({100 * n / len(all_labels):.0f} %)" for s, n in zip(stages, counts)}