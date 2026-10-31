# Results log — `<your track>`, `<your team>`

> **Copy this file into YOUR team's project repository** (not this scaffold repo) as
> `RESULTS.md`, and add one row per iteration as you go — not the night before the deadline.
> It exists because Chapter 16 §16.3 defines an iteration as _done_ only when it (1) runs end
> to end to a result, (2) reports the primary metric **with its spread**, (3) is committed with
> a note saying what changed and why, and (4) is at least as good as the previous iteration —
> **or** says in writing why the change was kept anyway. This table is where (2), (3) and (4)
> land; `git log` is where (1) becomes checkable. It also makes writing the report an assembly
> job rather than an archaeology project.
>
> **This file is graded.** `CAPSTONE_REPORT_RUBRIC.md` **Criterion 9 — Iteration & revision
> history (3 pts)** takes `RESULTS.md` as its evidence, and it asks for one specific thing that
> a forward-only log cannot show: **at least one earlier decision you went back and changed
> because of a downstream result**, with the symptom that sent you back named. A row that
> _lowered_ the headline metric and was kept for a stated reason is full-marks evidence, not a
> weakness. Rows here are also direct evidence for "Reproducibility & engineering" and "Report
> quality & defence".

**Track:** `sleep_edf` · **Split unit:** `subject` · **Primary metric:** `Cohen's κ` ·
**Evaluation mode(s):** `new-subject`

## Iteration log

Paste the metric straight from the harness — `rep["summary"]` prints the required shape, e.g.
`mean cohens_kappa 0.61 (sd 0.12, range 0.34-0.73 across 8 subjects)`. A pooled number with no
spread is half a result.

| #   | Date       | What changed & why (one line)                                                                                                                                                                                                                                                                                                         | Primary metric **with spread**                                                                                                                                                                                              | Better than previous? | If not — why it was kept                                                                                                                                                                                                                                               | Commit    |
| --- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | 2026-10-06 | supplied baseline, unchanged (RF, `imbalance="balanced"`, no preprocessing, default Welch features) — establish the floor; 3 subjects (`subset=[0,1,2]`), leave-one-subject-out                                                                                                                                                       | mean κ 0.720 (sd 0.119, range 0.589–0.822 across 3 subjects)                                                                                                                                                                | — (baseline)          | —                                                                                                                                                                                                                                                                      | `a1b2c3d` |
| 2.1 | 2026-10-12 | Imbalance: `imbalance="none"` instead of `"balanced"` (one change; same 11 features, 3 subjects, LOSO, seed 0) — does class weighting help the rare N1 class?                                                                                                                                                                         | mean cohens_kappa 0.764 (sd 0.085, range 0.668–0.831 across 3 subjects); macro-F1 0.695 (was 0.622); N1 recall 0.35 (was 0.20); per subject: SC400 0.589→0.668, SC401 0.822→0.831, SC402 0.749→0.792 (all 3 up)             | yes                   | — (provisional: re-test after cropping changes the class balance)                                                                                                                                                                                                      | `94c2db5` |
| 2.2 | 2026-10-15 | (preprocessing) Cropped each night to first/last non-W epoch ±30 min (see `tracks/sleep_crop.py`) - removes ~14 h/night of daytime Wake (W 68 % → 15 % of epochs); everything else as row 2.1 (`imbalance="none"`, 3 subjects, LOSO, seed 0)                                                                                          | mean cohens_kappa 0.580 (sd 0.193, range 0.358–0.694 across 3 subjects) (was before cropping: 0.764, sd 0.085, range 0.668–0.831); macro-F1 0.644 (was before cropping: 0.695); accuracy 0.711 (was before cropping: 0.885) | no                    | Kept. Before cropping, most epochs (~68 %) were daytime Wake, which is easy to separate from sleep. Cropping answers to the actual task, and the lower κ is a more honest estimate, not a worse pipeline.                                                              | `2d2126a` |
| 2.3 | 2026-10-15 | (preprocessing) High-pass filter on the EEG channel at 0.3 Hz (`preprocess="denoise"`, `baseline="highpass"`, `hp_fc=0.3`). The EEG spectrum showed very high power below ~0.5 Hz (baseline drift, highest in W; likely eye movements, movement and sweat); the filter attenuates everything below 0.3 Hz. Everything else as row 2.2 | mean cohens_kappa 0.597 (sd 0.178, range 0.392–0.706 across 3 subjects) ; macro-F1 0.657 ; accuracy 0.722                                                                                                                   | yes (small)           | The gain in mean κ (+0.017) is smaller than the spread across subjects, so it is not a clear improvement on its own; the lowest per-subject κ improved (0.358 → 0.392).                                                                                                | `6078dbd` |
| 2.4 | 2026-10-15 | (preprocessing) Band-pass filter on the EEG channel 0.3–35 Hz (`preprocess="bandpass"`, `eeg_band=(0.3, 35)`). Removes the baseline drift below 0.3 Hz (as row 2.3) and the part of the muscle (EMG) contamination in the EEG that lies above 35 Hz. The EOG and chin-EMG channels are not filtered. Everything else as row 2.2       | mean cohens_kappa 0.608 (sd 0.154, range 0.431–0.697 across 3 subjects) ; macro-F1 0.666 ; accuracy 0.729                                                                                                                   | yes                   | Kept. The gain in mean κ (+0.028) is within the spread across subjects, but almost all of it comes from the worst subject SC400 (0.358 → 0.431; SC401 0.694 → 0.696, SC402 0.688 → 0.697), and N3 recall improves (0.53 → 0.64). Best of the 3 planned configurations. | `6078dbd` |
| 2.5 |            |                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                             | yes / no              |                                                                                                                                                                                                                                                                        |           |
| 3.1 | 2026-10-31 | (features) + `relpow`: relative band powers, log total power, log δ/θ, θ/α, α/β (20 features). Everything else as row 2.4 | mean cohens_kappa 0.614 (sd 0.165, range 0.424–0.710 across 3 subjects); macro-F1 0.673; accuracy 0.733 | no measurable difference (+0.006) | Not kept: below the 0.02 rule, and the worst subject went down (SC400 0.431 → 0.424) | `7804a53` |
| 3.2 | 2026-10-31 | (features) + `spindle`: sigma-band spindle count, max envelope / night median, sigma peak prominence (14 features). Everything else as row 2.4 | mean cohens_kappa 0.674 (sd 0.107, range 0.550–0.739 across 3 subjects); macro-F1 0.709; accuracy 0.772 | yes (+0.066; all 3 subjects up) | — | `7804a53` |
| 3.3 | 2026-10-31 | (features) + `eogemg`: EOG slow/rapid eye-movement power and deflection count, chin-EMG level / relative-to-night / variability (17 features). Everything else as row 2.4 | mean cohens_kappa 0.645 (sd 0.159, range 0.462–0.750 across 3 subjects); macro-F1 0.703; accuracy 0.757 | yes (+0.037; all 3 subjects up) | — | `7804a53` |
| 3.4 | 2026-10-31 | (features) + `pz`: 5 band powers + spectral entropy from EEG Pz-Oz, band-passed 0.3–35 Hz like Fpz-Cz (17 features; `load()` now reads Pz-Oz). Everything else as row 2.4 | mean cohens_kappa 0.667 (sd 0.136, range 0.510–0.756 across 3 subjects); macro-F1 0.716; accuracy 0.771 | yes (+0.059; all 3 subjects up) | — | `7804a53` |
| 3.5 | 2026-10-31 | (features) `night_norm`: every one of the 11 features robust-z-scored within its own night (median/IQR; no labels, no other recording). Everything else as row 2.4 | mean cohens_kappa 0.674 (sd 0.061, range 0.604–0.714 across 3 subjects); macro-F1 0.707; accuracy 0.768 | yes (+0.066; worst subject +0.174, sd 0.154 → 0.061) | — | `7804a53` |
| 3.6 | 2026-10-31 | (features) `context`: features of the previous and next epoch appended (33 features). Everything else as row 2.4 | mean cohens_kappa 0.628 (sd 0.214, range 0.381–0.762 across 3 subjects); macro-F1 0.691; accuracy 0.743 | mean +0.020, but worst subject down | Not kept: SC400 0.431 → 0.381 and the spread grew (sd 0.154 → 0.214); prediction "largest gain" falsified | `7804a53` |
| 3.7 | 2026-10-31 | (features) combination by the pre-written rule (raise mean κ AND not lower worst-subject κ): `spindle + eogemg + pz + night_norm` (26 features). Everything else as row 2.4 | mean cohens_kappa 0.713 (sd 0.080, range 0.621–0.768 across 3 subjects); macro-F1 0.745; accuracy 0.795 | yes (+0.105 vs 2.4; all 3 subjects up: SC400 0.431 → 0.621, SC401 0.696 → 0.768, SC402 0.697 → 0.751) | — (but chosen on the same folds it is scored on; see detail) | `7804a53` |
| 4.1 |            |                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                             | yes / no              |                                                                                                                                                                                                                                                                        |           |
| 4.2 |            |                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                             | yes / no              |                                                                                                                                                                                                                                                                        |           |

_"Better" means better under the same honest harness — same split unit, same evaluation mode,
same seed. A change that lowers the metric can still be the right call (simpler, faster, more
robust across subjects, removes a leak). Say so in the column instead of quietly reverting it:
"kept — κ fell 0.02 but the worst-subject κ rose from 0.18 to 0.31" is a stronger result than a
silent higher mean._

- **Iteration 1 detail (supplied baseline, subject-wise LOSO, n = 3 subjects)**
  - Pooled over all folds: κ 0.729 · macro-F1 0.622 · accuracy 0.868
  - Per-subject κ: mean 0.720, sd 0.119, range 0.589–0.822
  - Note: accuracy (0.868) is well above macro-F1 (0.622); Wake dominates the epochs
    (~69% on Sleep-Cassette), so accuracy is inflated — read κ / macro-F1 / confusion matrix.
  - Yardstick: human inter-rater κ ≈ 0.76; published subject-wise models ≈ 0.79–0.82.
  - Prediction made before running: <TODO>
  - Leakage demo: random 5-fold κ = 0.899, subject-wise κ = 0.729, gap = +0.170

- **Iteration 2.1 detail (`imbalance="none"` vs `"balanced"`, same features, subject-wise LOSO, n = 3 subjects)**
  - Pooled: κ 0.769 (was 0.729) · macro-F1 0.695 (was 0.622) · balanced accuracy 0.670 (was 0.592) · accuracy 0.885 (was 0.868)
  - Per-subject κ: SC400 0.589→0.668, SC401 0.822→0.831, SC402 0.749→0.792 - all 3 up, largest gain on the worst subject
  - Confusion-matrix cells that moved (row-normalised): N3→N3 0.34→0.58 and N3→W 0.35→0.13 (the main gain);
    N1→N1 0.20→0.35 (N1→W 0.34→0.27, N1→N2 0.34→0.27); REM→REM 0.54→0.56; N2→N2 0.91→0.89; W→W 0.97 unchanged
  - Remaining errors: REM→N2 0.35, N3→N2 0.29, N1 split between W and N2; worst subject SC400 macro-F1 0.504
  - Possible explanation (not tested): with only 2 training subjects per fold, heavily up-weighted N3/N1 epochs may make
    the trees fit those subjects' patterns, which then transfer poorly to the held-out subject
  - Prediction made before running: weighting would help N1 - falsified on this data
  - Provisional: re-test after cropping (iteration plan row 2), since cropping changes the class balance

- **Iteration 2.2 detail (cropping to sleep period ±30 min, `imbalance="none"`, subject-wise LOSO, n = 3 subjects)**
  - Both runs were made on the same machine, with the same code and the same 3 subjects; only the cropping differs
  - Before cropping (reproduces row 2.1 exactly): κ mean 0.764, sd 0.085, range 0.668–0.831 · macro-F1 0.695 · accuracy 0.885
  - After cropping ±30 min: κ mean 0.580, sd 0.193, range 0.358-0.694 · macro-F1 0.644 · accuracy 0.711
  - Per-subject κ (before → after cropping): SC400 0.668 → 0.358, SC401 0.831 → 0.694, SC402 0.792 → 0.688. SC400 drops most and drives the larger spread
  - Confusion matrix (pooled over all 3 subjects, row-normalised): the main change is W→W 0.97 → 0.66; night-time Wake is now confused with N1 (0.13), N2 (0.12) and N3 (0.08). N1→N1 improves 0.35 → 0.43; the other stages are almost unchanged
  - Possible explanation (not tested): W→N3 may come from movement artifacts during night-time awakenings (large slow deflections that resemble delta waves). To be checked in the signal diagnosis before choosing a filter
  - Hours per night: 22.1-23.7 h before → 7.0-9.9 h after (each night is cropped at its own first and last sleep epoch)
  - Epochs per stage: N1 / N2 / N3 / REM unchanged (596 / 2792 / 932 / 1028); only Wake epochs were removed (from 11340 to 943); Wake share ~68 % → ~15 %
  - Why the metrics dropped:
    - Before cropping, ~68 % of the epochs were Wake, and most of it was daytime wakefulness (movement, high chin EMG, eyes open). It looks very different from sleep, so the model classifies it correctly almost every time.
    - This inflated accuracy and κ: a large part of the score came from the easy wake/sleep distinction, not from sleep staging.
    - After cropping, Wake is ~15 % of the epochs, and it is mostly night-time Wake (falling asleep, short awakenings). This looks similar to N1 and is much harder to classify.
    - Conclusion: κ fell (0.764 → 0.580) because the easy epochs were removed, not because the pipeline got worse.
  - Spread across subjects doubled (sd 0.085 → 0.193): performance during the sleep period varies a lot between subjects
  - Prediction made before running: <TODO>

- **Planned comparison: EEG review before filter choice (written before running filter)**
  - Signal diagnosis on the cropped nights:
    - Quality control: 0 flat epochs, 0 epochs > 500 µV, 1 clipped epoch in total (from SC4022E0); median peak 55-89 µV per night → no broken data, no epochs rejected
    - Powerline: no line at 50 Hz in the PSD → no notch filter
    - Slow artifacts / baseline wander: very high power below ~0.5 Hz, highest in W (as high as in N3). Likely eye movements and blinks, movement and sweat. This matches the W→N3 errors in row 2.2 → Candidate filtering: high-pass at 0.3 Hz (not higher, to keep the 0.5-2 Hz delta waves that define N3)
    - Muscle (EMG) shelf: flat, ~10× higher power above ~20 Hz in W than in the sleep stages → noise for the EEG, but also a marker of Wake → Candidate filtering: band-pass 0.3-35 Hz, to test whether removing it helps or hurts
    - Signal that must be preserved: delta waves in N3, K-complexes in N2, spindle peak at ~13-14 Hz in N2
  - Plan: 3 configurations, all on cropped data with `imbalance="none"` (as row 2.2), 3 subjects, LOSO, seed 0:
    1. no filter (is row 2.2)
    2. high-pass 0.3 Hz (`preprocess="denoise"`, `baseline="highpass"`, `hp_fc=0.3`)
    3. band-pass 0.3-35 Hz (`preprocess="bandpass"`, `eeg_band=(0.3, 35)`)
  - Not tested: notch (because no 50 Hz line); wavelet denoising (because no frequent spikes seen in the diagnosis); epoch rejection (because no broken epochs)
  - Prediction made before running: <todo>

- **Iteration 2.3-2.4 detail (filter comparison, 3 configurations as planned, cropped data, `imbalance="none"`, subject-wise LOSO, n = 3 subjects)**
  - Results (mean κ, sd, range across subjects · macro-F1 · accuracy):
    - no filter (= row 2.2): 0.580, sd 0.193, range 0.358-0.694 · 0.644 · 0.711
    - high-pass 0.3 Hz (row 2.3): 0.597, sd 0.178, range 0.392–0.706 · 0.657 · 0.722
    - band-pass 0.3-35 Hz (row 2.4): 0.608, sd 0.154, range 0.431-0.697 · 0.666 · 0.729
  - Both filters improve all three metrics; band-pass is best on all of them
  - Per-subject κ, band-pass vs.(→) no filter: SC400 0.358 → 0.431 (+0.073), SC401 0.694 → 0.696 (+0.002), SC402 0.688 → 0.697 (+0.009). Almost the whole gain comes from subject SC400; the spread shrinks (sd 0.193 → 0.154)
  - Size of the effect: the gain in mean κ (+0.028) is smaller than the spread across subjects, so with 3 subjects it is not a reliable improvement of the mean. The more robust finding is the improvement of the worst subject and the smaller spread
  - Confusion matrix (pooled, row-normalised), band-pass vs. no filter: N3→N3 0.53 → 0.64 and N3→N2 0.35 → 0.26 (the main change); W→N3 unchanged (0.08); other cells almost unchanged
  - Hypothesis from iteration 2.2 not supported: removing slow activity did NOT reduce W→N3, so those errors are not caused by drift below 0.3 Hz
  - Removing EEG above 35 Hz did not hurt Wake detection, likely because the chin-EMG channel is not filtered and still carries the muscle information

- **Diagnosis addendum (2026-10-22): EOG/EMG contamination check, done afterwards to re-check the filter choice**
  - Why: the first diagnosis (rows 2.3-2.4) only looked at the EEG channel. Chapter 8 in the course book also asks to screen the EEG for leakage from the eyes and muscles, using the EOG and chin-EMG channels as references.
  - Eye movements: per-epoch correlation between EEG and horizontal EOG in 0.5-5 Hz. (|r| from 0 = no correlation, to 1 = identical curves)
    - Median |r|: W => 0.13, N1 => 0.10, N2 => 0.09, N3 => 0.11, REM => 0.11; epochs with |r| > 0.5: ≤ 1 % in every stage
    - Conclusion: no measurable leakage of horizontal eye movements into the EEG. No EOG correction applied. Eye movements also do not explain the W → N3 errors
  - Muscle activity: Spearman correlation between EEG band power and chin-EMG level, per night, averaged over the 6 nights
    - All epochs: 0.5-4 Hz +0.25, 4-8 +0.10, 8-12 +0.17, 12-16 +0.10, 16-20 +0.31, 20-35 +0.35, 35-45 +0.36
    - Only N2 epochs: 0.5-4 Hz +0.10, 4-8 -0.11, 8-12 -0.08, 12-16 -0.09, 16-20 -0.01, 20-35 +0.09, 35-45 +0.13
    - Reading: across all epochs the correlation is moderate and grows with frequency, but most of it disappears within a single stage. It mainly reflects that Wake differs from sleep, not leakage. Within N2 the leakage is low.
    - Conclusion: the band-pass removes the part above 35 Hz; the low leakage left in 20-35 Hz is accepted to keep the whole beta band (16-30 Hz). A 30 Hz edge would remove more of it but also part of the beta band (not tested).
  - Effect on the filter choice: none. Band-pass 0.3-35 Hz (row 2.4) is kept; no EOG correction and no extra EMG handling added
  - Status of the W→N3 hypothesis from row 2.2: drift below 0.3 Hz (rows 2.3-2.4) and eye movements are ruled out. Movement artifacts during night-time awakenings were not tested directly. If they are the cause, a filter cannot remove them, because they overlap the 0.5-4 Hz delta band.

- **Coloured-noise check (2026-10-23)**: line fit to the log-log EEG PSD per stage (Welch on whole 30s epochs for finer frequency resolution, averaged over all epochs of each stage)
  - How to read it: a PSD slope of 0 means white noise, -1 pink (1/f) and -2 brown (1/f²). Brown noise is drift, and drift is removed with a high-pass filter. Pink noise is often physiology, not removed.
  - 0.1-0.5 Hz slope: W +2.16, N1 +1.30, N2 +1.78, N3 +2.80, REM +1.36. All positive: the power rises from ~0.2 Hz up to a peak at roughly 0.3-1 Hz.
  - Correction to rows 2.3-2.4: the low frequency power was described there as "baseline drift below 0.5 Hz". That description is not accurate. It is a slow peak, not drift. The filter choice is unchanged.
  - 1-30 Hz slope: W -1.90, N1 -1.83, N2 -2.59, N3 -2.95, REM -1.99. The shape lies between pink and brown, and N2/N3 are steeper than brown
  - The shape alone does not tell whether it is contamination or physiology, and here it can be physiology because it changes systematically with sleep stage (steepest in deep sleep) and it carries known rhythms on top (spindle peak at ~13-14 Hz in N2)
  - The remedy for brown noise (a high-pass) would have to be raised several Hz to change this shape, which would remove the 0.5-4 Hz delta waves that define N3. It is therefore kept. | `ef7f04b` |

- **Planned comparison: feature extraction, iteration 3 (written 2026-10-31, BEFORE running any of it)**
  - Starting point (the reference for every row 3.x): row 2.4 = cropped ±30 min, EEG band-pass 0.3-35 Hz, the 11 supplied features, `imbalance="none"`, RF, 3 subjects, LOSO, seed 0 → mean κ 0.608 (sd 0.154, range 0.431-0.697). Re-run on 2026-10-31 on a second machine: identical.
  - Errors the new features should target (row 2.4 confusion matrix): night-time W → N1/N2/N3 (W recall 0.66), N1 split between W and N2 (recall 0.42), N3 → N2 (0.26), REM → N2; worst subject SC400 (κ 0.431).
  - Signal check done before choosing features: in Sleep-Cassette the `EMG submental` channel is stored at **1 Hz** (30 samples per 30-s epoch; it is already an amplitude envelope, upsampled to 100 Hz by the loader). So the supplied `emg_rms` is just the mean chin-tone level, and no EMG frequency feature is possible. The EEG Pz-Oz channel (100 Hz) is in every file but the loader never reads it.
  - Comparison budget: **7 configurations**, fixed now. Rows 3.1-3.6 each add ONE feature group on top of row 2.4 (everything else unchanged); row 3.7 combines the groups that passed the rule below. Nothing else is tried on these folds.
    1. `relpow` — relative band power (each band / 0.5-30 Hz power) + log total power + log ratios δ/θ, θ/α, α/β. Why: absolute power depends on electrode impedance and skull, so it differs between subjects; ratios do not.
    2. `spindle` — sigma-band (11-16 Hz) spindle detector: band-pass, Hilbert envelope, threshold = 2.5 × the night's median envelope, events 0.5-2 s → spindle count, max envelope / night median, sigma peak prominence in the PSD. Why: spindles define N2 (AASM).
    3. `eogemg` — EOG: log power 0.3-1 Hz (slow eye movements, N1) and 1-5 Hz (rapid eye movements, REM), count of large EOG deflections; chin EMG: log level, level relative to the night's 10th percentile (REM atonia is relative to the person's own baseline), within-epoch variability. Why: REM vs N2 and N1 vs W are defined by eyes and muscle tone, not by EEG alone.
    4. `pz` — the same 5 band powers + spectral entropy from EEG Pz-Oz (also band-passed 0.3-35 Hz). Why: posterior alpha marks eyes-closed Wake and its loss marks N1.
    5. `night_norm` — every feature robust-z-scored within its own night (median / IQR). Why: target the subject-level shift behind SC400. Leakage note: the statistics come from one recording only and never from labels, so nothing crosses the subject split; at hold-out time it uses the test night's own unlabelled signal.
    6. `context` — the features of the previous and the next epoch appended. Why: AASM scoring itself uses neighbouring epochs; N1 and REM are often decided by what comes before/after.
    7. combination of every group from 1-6 that (a) raises mean κ AND (b) does not lower the worst-subject κ.
  - Rule for "helped": a change in mean κ smaller than about 0.02 is read as "no measurable difference" (sd across subjects is 0.15); the per-subject κ and the per-class recall are read before the mean.
  - Predictions (made before running): context gives the largest gain (N1, REM); night_norm helps the worst subject SC400 most; eogemg raises REM recall; relpow small gain; spindle small and mostly N2; pz smallest (Fpz-Cz already sees alpha).

- **Iteration 3.1-3.7 detail (feature groups, 7 configurations as planned, cropped + band-passed data, `imbalance="none"`, subject-wise LOSO, n = 3 subjects; code `tracks/sleep_features.py`, run `notebooks/features.ipynb`)**
  - The reference re-run inside the same notebook reproduces row 2.4 exactly (0.608, sd 0.154, range 0.431-0.697), so every difference below is the feature group's doing.
  - Per-subject κ (SC400 / SC401 / SC402) and recall (W / N1 / N2 / N3 / REM):
    - 2.4 reference: 0.431 / 0.696 / 0.697 · 0.66 / 0.42 / 0.91 / 0.64 / 0.57
    - 3.1 relpow: 0.424 / 0.709 / 0.710 · 0.62 / 0.44 / 0.91 / 0.65 / 0.61
    - 3.2 spindle: 0.550 / 0.731 / 0.739 · 0.71 / 0.45 / 0.93 / 0.65 / 0.70
    - 3.3 eogemg: 0.462 / 0.750 / 0.724 · 0.71 / 0.39 / 0.92 / 0.70 / 0.63
    - 3.4 pz: 0.510 / 0.735 / 0.756 · 0.75 / 0.40 / 0.93 / 0.75 / 0.59
    - 3.5 night_norm: 0.604 / 0.714 / 0.704 · 0.60 / 0.47 / 0.89 / 0.74 / 0.81
    - 3.6 context: 0.381 / 0.762 / 0.740 · 0.75 / 0.51 / 0.90 / 0.62 / 0.55
    - 3.7 combined: 0.621 / 0.768 / 0.751 · 0.73 / 0.51 / 0.89 / 0.73 / 0.83
  - Reading against the spread: single-group gains (+0.04 to +0.07) are smaller than the across-subject sd of 0.15, so the mean alone is not evidence. What is: for spindle, eogemg, pz and night_norm **every one of the 3 subjects** moved up, i.e. the paired per-subject change is consistent.
  - Predictions vs results: context "largest gain" → **falsified** (worst subject down, spread up; with only 2 training subjects per fold, 3× the columns seems to let the forest fit those two people — not tested further). night_norm "helps SC400 most" → confirmed (+0.174). spindle "small" and pz "smallest" → wrong, both among the largest. eogemg "REM up" → only modestly (0.57 → 0.63); the big REM gain came from night_norm (0.81). relpow "small gain" → no measurable difference.
  - Confusion matrix 2.4 → 3.7 (pooled, row-normalised): REM→N2 0.33 → 0.06 (the main gain), W→N2 0.13 → 0.02, W→N3 0.08 → 0.00 (the W→N3 errors that rows 2.2-2.4 could not remove with filters are gone), N3→N3 0.64 → 0.73. **New/remaining errors:** W→N1 grew 0.12 → 0.22, N1→N2 0.23, N3→N2 unchanged at 0.26.
  - Honest caveat on 3.7: the combination was chosen by a rule written in advance, but on the same 3 folds it is scored on, so its +0.105 is optimistically biased (selection effect). Configurations compared in iteration 3: 7 (+ the reference re-run).
  - Leakage: night_norm, the spindle threshold, the EOG threshold and the EMG floor use statistics of one night only and never the labels; nothing is fitted across recordings, so building features before the folds stays safe. They do use the whole unlabelled night, so the pipeline is offline (fine for retrospective scoring, not for a live monitor).

## ⚠️ Before you fill in many rows — the garden of forking paths

The harness guarantees that **no single run** leaks a subject. It cannot guarantee anything
about the _sequence_ of runs. Every row in the table above is scored on the **same**
group-aware folds, and those are the same folds that produce the number you will report. Try
twelve configurations against one held-out set and report the best, and the winner was chosen
partly because it happens to suit _these particular subjects_. Its margin over the runner-up is
optimistically biased, and nothing in the report will look wrong. This is a **selection effect**,
not a leak — which is exactly why the leakage guard cannot catch it, and why it has to be
handled by how you _plan_ the work rather than by the code.

It bites hardest here because the cohorts are small: a dozen comparisons on five or six subjects
is a great deal of selection pressure on very little data.

Two defensible ways to handle it. **Say in the report which one you used** — Criterion 7 grades
the quality of the comparison, and this is part of that quality:

| approach                        | what you do                                                                                                                                                                | what it costs                                                                                                                             |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **an explicit development set** | hold out a few groups _up front_ as a DEV set; compare every design option on DEV only; run the chosen pipeline **once** on the untouched evaluation folds and report that | fewer groups serving each purpose — painful on these cohorts — and a noisier DEV estimate                                                 |
| **a comparison budget**         | decide in advance how many configurations you will compare (a handful, not a sweep), write them into this file **before** you run them, and report the count               | you may miss a better option, and you have to resist re-opening the budget once you have seen the numbers — which is the whole discipline |

Either way, two habits that cost nothing:

- **Record the count.** "We compared 6 configurations" belongs in the report. A team that
  compares six and says so is doing better science than one that compares twenty and shows a
  longer table.
- **Read a small margin as no margin.** If the difference between two options is smaller than
  the spread across your subjects/folds, it is not a result. Say "no measurable difference; we
  kept the simpler one" — that sentence earns marks, and claiming the 0.01 does not.

**Related, and equally invisible: _where_ your preprocessing is fitted.** The notebook builds
features for every recording **before** `evaluate()` cuts the folds. That is safe for everything
the scaffold ships, because all of it is **stateless** — a fixed filter, or a threshold estimated
from one epoch's own samples. It stops being safe the moment you add a stage that **learns**:
CSP, PCA/ICA, a cohort-wide z-score, a learned artifact template. Fit one of those over all the
recordings and every held-out subject has already shaped the transform that built the training
features — and `assert_no_subject_leak` will still pass, because it checks group ids and cannot
see what a filter was learned from. A learned stage must be fitted **inside** the fold: as a step
in the classifier pipeline (cloned and refit per fold) or via `select_features()`. If you added
one, record here which of the two you used.

## Decision log — the choices behind the numbers

Rows above say _what happened_; this says _what you chose and why_, which is what §16.4 asks you
to make traceable and what the report's defence is built from. There is no single correct
pipeline here — the scaffold deliberately ships options, not answers. One line per decision;
add rows as the pipeline grows, and note the alternative you rejected.

| Pipeline module                      | Option chosen                                                   | Alternative(s) considered                                                                                                 | Why this one (one sentence)                                                                                                                                                          | Iteration | Revised later?                                                                          |
| ------------------------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- | --------------------------------------------------------------------------------------- |
| 1. Data loading                      | _e.g._ 8 subjects, both nights                                  | more subjects, one night each                                                                                             | subject-level split needs both nights inside one group                                                                                                                               | 1         | —                                                                                       |
| 2. Preprocessing                     |                                                                 |                                                                                                                           |                                                                                                                                                                                      |           |                                                                                         |
| 3. Feature extraction                | supplied 11 + `spindle` + `eogemg` + `pz` + `night_norm` (26 features) | `relpow` (no measurable difference), `context` (lowered the worst subject) | Each kept group raised κ for all 3 subjects on its own; the two rejected ones failed the rule written before running. Configurations compared: 7 | 3 | — |
| 4. Feature selection                 | _e.g._ `select="none"`                                          | ANOVA `SelectKBest`, tree importances                                                                                     | 14 features vs. ~1 800 epochs — pruning risked more than it saved                                                                                                                    | 1         | _e.g._ **yes, iter 4** — `select_k=20` was a no-op (harness said so); switched to `k=6` |
| 5. Classification, incl. `imbalance` | `imbalance="none"` (provisional), random forest kept            | `"balanced"` (default); other learners not needed — course allows keeping one learner and spending iterations on features | On uncropped data, class weighting lowered κ for all 3 subjects (mean 0.720 vs 0.764) and N1 recall (0.20 vs 0.35); re-test after cropping. Configurations compared at this stage: 2 | 2         | pending                                                                                 |
| 6. Inference                         |                                                                 |                                                                                                                           |                                                                                                                                                                                      |           |                                                                                         |
| 7. Reporting                         |                                                                 |                                                                                                                           |                                                                                                                                                                                      |           |                                                                                         |
| Environment                          | Python 3.11 + `requirements-lock.txt` + `requirements-real.txt` | Python 3.14 with unpinned packages                                                                                        | On Python 3.14 the same baseline gave κ 0.704 instead of 0.720; with the pinned versions every team member reproduces 0.720 exactly                                                  | 1         | —                                                                                       |

## Revisions — the ones that went **backwards** (Criterion 9's actual evidence)

Adding iterations forward is a to-do list. What this section wants is the place a number
downstream sent you back **up** the pipeline. One row is enough; two is a good project.
The notebook's "Decision points on this track" section has a symptom → stage table to
diagnose from.

| #   | The downstream result that triggered it   | Which earlier decision it indicted       | What you changed                           | What happened to the metric                              |
| --- | ----------------------------------------- | ---------------------------------------- | ------------------------------------------ | -------------------------------------------------------- |
| 1   | _e.g._ worst-subject κ 0.14 vs. mean 0.61 | stage 2 — no per-recording normalisation | z-scored band powers within each recording | mean κ 0.61 → 0.59, **worst subject 0.14 → 0.38** — kept |
| 2   | worst-subject κ stayed far below the others through rows 2.2-2.4 (SC400 0.431 vs ~0.70); filters only moved it a little | stage 3 — the supplied features are absolute amplitudes/powers, so a subject whose overall EEG level differs is mis-scaled | robust z-score of every feature within its own night (row 3.5) | mean κ 0.608 → 0.674, **worst subject 0.431 → 0.604**, sd 0.154 → 0.061 — kept |

## Who did what

One line per person per iteration — the honest-disclosure requirement of §16.7, and the evidence
`INDIVIDUAL_ASSESSMENT.md` asks for. The seven modules do **not** have to map one-to-one onto
people: one person may own several modules, two people may share one, and ownership may rotate
between iterations. Record what actually happened.

| Iteration | Who | Modules / tasks owned | Reviewed by |
| --------- | --- | --------------------- | ----------- |
| 1         |     |                       |             |

## Final numbers (fill in once, at the end)

|                                                                      | Value | Under what split                                               |
| -------------------------------------------------------------------- | ----- | -------------------------------------------------------------- |
| Primary metric, development (mean + spread)                          |       |                                                                |
| Secondary metrics (macro-F1 / balanced accuracy / per-class recall)  |       |                                                                |
| Held-out set — **scored once, never tuned against**                  |       |                                                                |
| Supplied baseline, same harness                                      |       |                                                                |
| Yardstick from the dataset card (human ceiling / benchmark / chance) |       |                                                                |
| **Configurations compared** before settling (a number)               |       | on DEV folds / on the evaluation folds — say which             |
| How option comparison was kept separate from final reporting         |       | _e.g._ "separate DEV groups" / "budget of 6, fixed in advance" |

_Grading: `CAPSTONE_REPORT_RUBRIC.md` (team, 30 pts) and `INDIVIDUAL_ASSESSMENT.md`
(individual, 10 pts)._
