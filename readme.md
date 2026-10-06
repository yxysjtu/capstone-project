# CM2013 Capstone — Sleep Staging (Sleep-EDF) Team Environment Guide

This guide helps you set up the environment on your own computer and use Jupyter notebooks to complete two tests in order:

1. **Smoke test**: use synthetic data to quickly confirm that the environment and code are working.
2. **Real data test**: download real Sleep-EDF data and run the course-provided baseline.

> The smoke test numbers are only a check that "the pipeline runs"; they are **not results and must not be written into the report**.

---

## 0. Prerequisites

- **Git** and **Python** are installed (version: `Python 3.11.9`; try to keep it consistent. Run `python --version` to check).
- **VS Code** is installed, with the Python and Jupyter extensions installed.
- Leave about 1–2 GB of disk space (real data cache plus dependencies).

## 1. Get the Code

```
git clone <team repository URL>
cd <repository directory>
```

At the repo root, you should see `tracks/`, `src/`, `notebooks/`, `requirements-lock.txt`, and `requirements-real.txt`.

## 2. Create a Virtual Environment and Install Dependencies

**Do not commit `.venv` to GitHub** (it is tied to your computer's paths and system). Only dependency manifests go in the repo; each person installs dependencies separately.

### Windows (PowerShell)

```
python -m venv .venv
.venv\Scripts\Activate.ps1
$env:PYTHONUTF8 = "1"
pip install -r requirements-lock.txt
pip install -r requirements-real.txt
pip install ipykernel
```

- After successful activation, `(.venv)` will appear at the beginning of the command line.
- If activation says "running scripts is disabled", first run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again.

### Mac / Linux

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-lock.txt
pip install -r requirements-real.txt
pip install ipykernel
```

### Notes

- `requirements-lock.txt`: core dependencies, with **versions pinned**, to ensure everyone has the same environment and reproducible results.
- `requirements-real.txt`: `mne==1.10.1` and `wfdb==4.3.0` required for real data. **Do not upgrade the versions casually**; upgrading may silently change data reading results.

## 3. Verify the Environment

In a terminal with the virtual environment activated, run:

```
python -c "import numpy, scipy, sklearn, matplotlib, pywt, mne, imblearn; print(numpy.__version__, scipy.__version__, sklearn.__version__, matplotlib.__version__, pywt.__version__, mne.__version__, imblearn.__version__)"
```

It should output:

```
2.2.6 1.15.3 1.7.2 3.10.9 1.8.0 1.10.1 0.14.2
```

If the versions do not match, or you get `ModuleNotFoundError`, the installation did not succeed. Do not continue yet.

## 4. Open the Notebook in VS Code

1. Open `notebooks/track_sleep_edf.ipynb`.
2. Click **Select Kernel → Python Environments** in the upper right, and choose the one whose path contains `.venv`. If it is not there, press `Ctrl+Shift+P`, run **Python: Select Interpreter**, choose `.venv\Scripts\python.exe`, then come back and select the kernel.
3. In the notebook, create a new cell and run the following code to confirm you are using the virtual environment:
   ```python
   import sys; print(sys.executable)
   ```
   The output path should contain `.venv`.

> The first code cell in the notebook adds the parent directory (`..`) to the import path, so **open it from the `notebooks/` folder inside the repo**; otherwise `sleep_edf` cannot be found.
>
> If after running you notice a `_bsp_repo` folder has appeared in the current directory, it means the import failed and the code silently cloned the original course repo. In this case, you are not using the team repo's code. Delete `_bsp_repo`, fix the path issue, restart the kernel, and run again.

## 5. Step 1: Smoke Test (Synthetic Data, Offline)


1. Keep `USE_REAL = IN_COLAB and False` unchanged in the first code cell (this uses synthetic data).
2. Run cells in order from the top through the "Get the data" cell. You should see `recordings: … | subjects: […]`.
3. Run the following `build_dataset` and `evaluate` cells. If it prints `Cohen's kappa` and `spread`, it passes.

## 6. Step 2: Real Data Test

**Do this step only after the smoke test passes.**

1. In the repo root, first create the cache folder so the data lands here (and will not be committed):
   ```
   mkdir data_cache
   ```
   Make sure `.gitignore` contains `data_cache/` and `.venv/`.
2. In the first code cell of the notebook, change
   ```python
   USE_REAL = IN_COLAB and False
   ```
   to
   ```python
   USE_REAL = True
   ```
   (The `and False` makes it always False, including locally. You do not need to delete the Colab-related code; only change this line.)
3. Run the "Get the data" cell. It downloads data for **3 subjects** (`subset=[0, 1, 2]`).
   - **The first download takes over 20 minutes.** During this time the cell will keep showing as running, with no progress bar; do not assume it is frozen. You can check whether `.edf` files are increasing in `data_cache/`.
   - After the download completes, it is cached locally and does not need to be downloaded again.
   - **Everyone should use the same subject subset** so the numbers match across team members.
4. After downloading, run the `build_dataset` and `evaluate` cells and look at κ, macro-F1, and `spread`.

**Reference numbers**: The team's first baseline run was `mean κ 0.720 (sd 0.119, range 0.589–0.822 across 3 subjects)`, pooled κ 0.729. Your results should be broadly consistent with this. If they differ a lot, first check: whether the number of subjects is 3 and whether dependency versions are consistent.

## 7. Common Issues

| Symptom | Cause and handling |
|---|---|
| `source` is not a command | You are on Windows; use `.venv\Scripts\Activate.ps1` |
| `UnicodeDecodeError: 'gbk' codec ...` | Run `$env:PYTHONUTF8 = "1"` before installing |
| Cannot find packages such as numpy | The VS Code kernel is not set to `.venv`, or the virtual environment is not activated |
| `ModuleNotFoundError: sleep_edf / adapter / bsp` | The notebook was not opened under `notebooks/`, or the repo is missing the `tracks` or `src` folders |
| During installation, no version satisfying the requirements is found | The Python version may be too old; switch to the same version as the team lead and recreate `.venv` |
| The cell keeps spinning after download | It may still be downloading; check whether files in `data_cache/` are increasing, and do not interrupt it midway |
| A `_bsp_repo` folder appears in the current directory | The import failed and it took the clone branch; see the note in Section 4 |

## 8. Important Notes

- **Do not commit**: `.venv/`, `data_cache/`.
- **Smoke test numbers are not results**; do not record them in `RESULTS.md` as the baseline.
- Before changing code, create a branch. Before merging, run `python sleep_edf.py` (smoke) once to confirm nothing is broken, then open a PR.
- The real-data baseline results and leakage test numbers should be recorded in `RESULTS.md` by the owner, with a comment under the corresponding ClickUp task.
