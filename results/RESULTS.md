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
| 3.1 |            |                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                             | yes / no              |                                                                                                                                                                                                                                                                        |           |
| 3.2 |            |                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                             | yes / no              |                                                                                                                                                                                                                                                                        |           |
| 3.3 |            |                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                             | yes / no              |                                                                                                                                                                                                                                                                        |           |
| 3.4 |            |                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                             | yes / no              |                                                                                                                                                                                                                                                                        |           |
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
  - Per-subject κ: SC400 0.589→0.668, SC401 0.822→0.831, SC402 0.749→0.792 — all 3 up, largest gain on the worst subject
  - Confusion-matrix cells that moved (row-normalised): N3→N3 0.34→0.58 and N3→W 0.35→0.13 (the main gain);
    N1→N1 0.20→0.35 (N1→W 0.34→0.27, N1→N2 0.34→0.27); REM→REM 0.54→0.56; N2→N2 0.91→0.89; W→W 0.97 unchanged
  - Remaining errors: REM→N2 0.35, N3→N2 0.29, N1 split between W and N2; worst subject SC400 macro-F1 0.504
  - Possible explanation (not tested): with only 2 training subjects per fold, heavily up-weighted N3/N1 epochs may make
    the trees fit those subjects' patterns, which then transfer poorly to the held-out subject
  - Prediction made before running: weighting would help N1 — falsified on this data
  - Provisional: re-test after cropping (iteration plan row 2), since cropping changes the class balance

- **Iteration 2.2 detail (cropping to sleep period ±30 min, `imbalance="none"`, subject-wise LOSO, n = 3 subjects)**
  - Both runs were made on the same machine, with the same code and the same 3 subjects; only the cropping differs
  - Before cropping (reproduces row 2.1 exactly): κ mean 0.764, sd 0.085, range 0.668–0.831 · macro-F1 0.695 · accuracy 0.885
  - After cropping ±30 min: κ mean 0.580, sd 0.193, range 0.358–0.694 · macro-F1 0.644 · accuracy 0.711
  - Per-subject κ (before → after cropping): SC400 0.668 → 0.358, SC401 0.831 → 0.694, SC402 0.792 → 0.688. SC400 drops most and drives the larger spread
  - Confusion matrix (pooled over all 3 subjects, row-normalised): the main change is W→W 0.97 → 0.66; night-time Wake is now confused with N1 (0.13), N2 (0.12) and N3 (0.08). N1→N1 improves 0.35 → 0.43; the other stages are almost unchanged
  - Possible explanation (not tested): W→N3 may come from movement artifacts during night-time awakenings (large slow deflections that resemble delta waves). To be checked in the signal diagnosis before choosing a filter
  - Hours per night: 22.1–23.7 h before → 7.0–9.9 h after (each night is cropped at its own first and last sleep epoch)
  - Epochs per stage: N1 / N2 / N3 / REM unchanged (596 / 2792 / 932 / 1028); only Wake epochs were removed (from 11340 to 943); Wake share ~68 % → ~15 %
  - Why the metrics dropped:
    - Before cropping, ~68 % of the epochs were Wake, and most of it was daytime wakefulness (movement, high chin EMG, eyes open). It looks very different from sleep, so the model classifies it correctly almost every time.
    - This inflated accuracy and κ: a large part of the score came from the easy wake/sleep distinction, not from sleep staging.
    - After cropping, Wake is ~15 % of the epochs, and it is mostly night-time Wake (falling asleep, short awakenings). This looks similar to N1 and is much harder to classify.
    - Conclusion: κ fell (0.764 → 0.580) because the easy epochs were removed, not because the pipeline got worse.
  - Spread across subjects doubled (sd 0.085 → 0.193): performance during the sleep period varies a lot between subjects, which motivates the next preprocessing steps
  - Prediction made before running: <TODO>

- **Planned comparison: EEG review before filter choice (written before running filter)**
  - Signal diagnosis on the cropped nights:
    - Quality control: 0 flat epochs, 0 epochs > 500 µV, 1 clipped epoch in total (from SC4022E0); median peak 55–89 µV per night → no broken data, no epochs rejected
    - Powerline: no line at 50 Hz in the PSD (50 Hz is also the Nyquist frequency at 100 Hz) → no notch filter
    - Slow artifacts / baseline wander: very high power below ~0.5 Hz, highest in W (as high as in N3). Likely eye movements and blinks, movement and sweat. This matches the W→N3 errors in row 2.2 → Candidate filtering: high-pass at 0.3 Hz (not higher, to keep the 0.5–2 Hz delta waves that define N3)
    - Muscle (EMG) shelf: flat, ~10× higher power above ~20 Hz in W than in the sleep stages → noise for the EEG, but also a marker of Wake → Candidate filtering: band-pass 0.3–35 Hz, to test whether removing it helps or hurts
    - Signal that must be preserved: delta waves in N3, K-complexes in N2, spindle peak at ~13–14 Hz in N2
  - Plan: 3 configurations, all on cropped data with `imbalance="none"` (as row 2.2), 3 subjects, LOSO, seed 0:
    1. no filter (is row 2.2)
    2. high-pass 0.3 Hz (`preprocess="denoise"`, `baseline="highpass"`, `hp_fc=0.3`)
    3. band-pass 0.3–35 Hz (`preprocess="bandpass"`, `eeg_band=(0.3, 35)`)
  - Not tested: notch (because no 50 Hz line); wavelet denoising (because no frequent spikes seen in the diagnosis); epoch rejection (because no broken epochs)
  - Prediction made before running: <todo>

- **Iteration 2.3-2.4 detail (filter comparison, 3 configurations as planned, cropped data, `imbalance="none"`, subject-wise LOSO, n = 3 subjects)**
  - Results (mean κ, sd, range across subjects · macro-F1 · accuracy):
    - no filter (= row 2.2): 0.580, sd 0.193, range 0.358–0.694 · 0.644 · 0.711
    - high-pass 0.3 Hz (row 2.3): 0.597, sd 0.178, range 0.392–0.706 · 0.657 · 0.722
    - band-pass 0.3–35 Hz (row 2.4): 0.608, sd 0.154, range 0.431–0.697 · 0.666 · 0.729
  - Both filters improve all three metrics; band-pass is best on all of them
  - Per-subject κ, band-pass vs.(→) no filter: SC400 0.358 → 0.431 (+0.073), SC401 0.694 → 0.696 (+0.002), SC402 0.688 → 0.697 (+0.009). Almost the whole gain comes from subject SC400; the spread shrinks (sd 0.193 → 0.154)
  - Size of the effect: the gain in mean κ (+0.028) is smaller than the spread across subjects, so with 3 subjects it is not a reliable improvement of the mean. The more robust finding is the improvement of the worst subject and the smaller spread
  - Confusion matrix (pooled, row-normalised), band-pass vs. no filter: N3→N3 0.53 → 0.64 and N3→N2 0.35 → 0.26 (the main change); W→N3 unchanged (0.08); other cells almost unchanged
  - Hypothesis from iteration 2.2 not supported: removing slow activity did NOT reduce W→N3, so those errors are not caused by drift below 0.3 Hz
  - Removing EEG above 35 Hz did not hurt Wake detection, likely because the chin-EMG channel is not filtered and still carries the muscle information

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
| 3. Feature extraction                |                                                                 |                                                                                                                           |                                                                                                                                                                                      |           |                                                                                         |
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
| 2   |                                           |                                          |                                            |                                                          |

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
