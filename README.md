
# UAD Toolkit

Open, reproducible toolkit for building the **Uniform Appearance Diagram (UAD)** from hue‑scaling data, following the workflow described in Abramov, Gordon, & Chan (2009, *Attention, Perception, & Psychophysics*).

## Install (editable)
```bash
pip install -e .
```

## Quickstart
```bash
uad from-csv examples/huescalingdata.csv --out out/obs01 --criterion 4.0 --min 330 --max 660
```

This will output:
- `out/obs01_uad_1nm.csv` (RG,YB at 1‑nm steps)
- `out/obs01_discrimination.csv` (Δλ per wavelength using city‑block threshold)
- `out/obs01_uad_trajectory.png`
- `out/obs01_discrimination.png`

## Data format
CSV columns (case-insensitive): `Lambda (nm)`, `% Red`, `% Yellow`, `% Green`, `% Blue`, `% Saturation` (optional). Percentages 0–100 or proportions 0–1.

## Reproducibility
- Functions are pure and tested with a smoke test under `tests/`.
- Example dataset and script are provided in `examples/` and `scripts/`.
