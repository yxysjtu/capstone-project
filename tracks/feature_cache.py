"""
tracks.feature_cache — save the feature matrix once, reuse it for modules 4-5.

Building features means reading every full night into memory (~250 MB a night)
and running stages 2-3. The result is tiny (~0.2 MB a night), and selection /
classification experiments only need that result. So whoever has the memory
builds it once with `save_features`, and everyone else calls `load_features`.

A cache is only valid for the stage 2-3 settings AND the code it was built with.
The file stores the settings (every feature-affecting cfg key, plus the cropping)
and a hash of every source file that computes the features (`CODE_FILES`), and
`load_features` refuses a file where either differs — a stale cache would
otherwise give old features under a new config or edited code with no error.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
from datetime import datetime

import numpy as np

DEFAULT_CROP = "crop_to_sleep(margin_min=30)"

_TRACKS = os.path.dirname(os.path.abspath(__file__))
_BSP = os.path.join(os.path.dirname(_TRACKS), "src", "bsp")
#: every file whose content changes the feature matrix: loading, cropping, filters, features
CODE_FILES = {name: os.path.join(_TRACKS, name)
              for name in ("sleep_edf.py", "sleep_crop.py", "SC-subjects.csv",
                           "sleep_features.py", "adapter.py")}
CODE_FILES.update({f"bsp/{name}": os.path.join(_BSP, name)
                   for name in ("sleep_pipeline.py", "biosignals.py")})


def _code_hashes():
    """Short hash of each file in CODE_FILES. Line endings are normalised first, so a
    Windows (CRLF) and a Mac/Linux (LF) checkout of the same commit agree."""
    out = {}
    for name, path in sorted(CODE_FILES.items()):
        with open(path, "rb") as f:
            out[name] = hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()[:12]
    return out


def _fingerprint(track, crop):
    """What decides the feature matrix: stage 2-3 cfg keys, cropping and the code."""
    cfg = track._cfg()
    keys = sorted(k for k in track.feature_cfg_keys() if k in cfg)
    return json.loads(json.dumps({"cfg": {k: cfg[k] for k in keys}, "crop": crop,
                                  "code": _code_hashes()}, default=str, sort_keys=True))


def _git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return None


def save_features(path, track, recs, X, y, groups, crop=DEFAULT_CROP):
    """Write X, y, groups (+ the settings they were built with) to `path` (.npz)."""
    records = np.concatenate([[r.meta.get("record", r.group)] * len(r.labels) for r in recs])
    info = {"fingerprint": _fingerprint(track, crop),
            "feature_names": track.feature_names(),
            "subjects": sorted({str(g) for g in groups}),
            "n_rows": int(len(y)),
            "git_commit": _git_commit(),
            "created": datetime.now().isoformat(timespec="seconds")}
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    np.savez_compressed(path, X=np.asarray(X), y=np.asarray(y).astype(str),
                        groups=np.asarray(groups).astype(str), records=records.astype(str),
                        info=np.array(json.dumps(info)))
    return info


def load_features(path, track, crop=DEFAULT_CROP, subjects=None):
    """Read a cache written by `save_features`; raise ValueError if it was built
    with different stage 2-3 settings than `track` has now, or (when `subjects`
    is given) for a different set of subjects."""
    with np.load(path, allow_pickle=False) as d:
        info = json.loads(str(d["info"]))
        if subjects is not None and info["subjects"] != sorted(subjects):
            raise ValueError(f"{path} holds subjects {info['subjects']}, not {sorted(subjects)}; rebuild it.")
        want = _fingerprint(track, crop)
        if info["fingerprint"] != want:
            got = info["fingerprint"]
            diff = sorted(k for k in set(got["cfg"]) | set(want["cfg"])
                          if got["cfg"].get(k) != want["cfg"].get(k))
            if got["crop"] != want["crop"]:
                diff.append("crop")
            diff += [f"code {name}" for name in sorted(set(got.get("code", {})) | set(want["code"]))
                     if got.get("code", {}).get(name) != want["code"].get(name)]
            raise ValueError(f"{path} was built with different stage 2-3 settings or code "
                             f"(differs in: {', '.join(diff)}); rebuild it.")
        return d["X"], d["y"], d["groups"], info
