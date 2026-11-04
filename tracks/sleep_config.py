"""
tracks.sleep_config — the team's current pipeline configuration, in ONE place.

Import it instead of copying the dict into notebooks:

    from sleep_config import CURRENT_CFG
    track = SleepEDFTrack(cfg=CURRENT_CFG)

Each module owner edits only their own line, and every change is logged as a new
row in results/RESULTS.md (which row this dict reproduces is noted below).
Reproduces RESULTS.md row 3.7: mean kappa 0.713 (sd 0.080, range 0.621-0.768,
3 subjects, LOSO). Nights must also be cropped with `sleep_crop.crop_to_sleep`.
"""

CURRENT_CFG = {
    # module 2 — preprocessing (rows 2.2-2.4)
    "preprocess": "bandpass",
    "eeg_band": (0.3, 35.0),
    "filter_channels": ("eeg", "eeg2"),      # eeg2 = Pz-Oz, filtered like Fpz-Cz
    # module 3 — feature extraction (rows 3.1-3.7, tracks/sleep_features.py)
    "feature_groups": ("spindle", "eogemg", "pz", "night_norm"),
    # module 4 — feature selection (rows 4.2-4.3): pass-through, all 26 features kept;
    # ANOVA k=12 and tree importance both lowered kappa for 9 of 10 subjects
    "select": "none",
    # module 5 — classification (rows 2.1, 4.1, 4.4): random forest, no class weights;
    # re-tested after cropping on 10 subjects (row 4.1): "balanced" gave no measurable gain
    "imbalance": "none",
}
