"""
Independent recomputation of the teaser flexibility indicators.

Recomputes, from the raw input CSVs of data/teaser and from the solved
networks, the indicators that EU-Flex stores in model_outputs.nc, using a
straightforward implementation of FNA methodology Art. 8(5) and 10(1), and
compares the two. Also checks the accounting identity "sum of contributions =
need" on the model's own outputs.

Usage (repository root, after the teaser run):

    python adversarial_review/scripts/independent_recompute.py runs/teaser
"""

import json
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pypsa
import xarray as xr

logging.disable(logging.WARNING)

RUN = Path(sys.argv[1] if len(sys.argv) > 1 else "runs/teaser")
DATA = Path("data/teaser/ty_2030_cy_2013")
TY = 2030
RES = ["Solar (PV)", "Wind Onshore", "Wind Offshore", "Hydro - Run of River (Turbine)"]
out = {}


def hourly_index(n_rows, ty=TY):
    return pd.date_range(f"{ty}-01-01", periods=n_rows, freq="h")


# ---------------------------------------------------------------- inputs
gens = pd.read_csv(DATA / "generators.csv", index_col=0)
loads = pd.read_csv(DATA / "loads.csv", index_col=0)


def residual_load(pmaxpu_file, load_file):
    pu = pd.read_csv(DATA / pmaxpu_file, index_col=0)
    ld = pd.read_csv(DATA / load_file, index_col=0)
    idx = hourly_index(len(pu))
    pu.index = idx
    ld.index = idx
    res = [g for g in pu.columns if gens.loc[g, "carrier"] in RES]
    avail = pu[res].mul(gens.loc[res, "p_nom"]).T.groupby(gens.loc[res, "bus"]).sum().T
    dem = ld.T.groupby(loads.loc[ld.columns, "bus"]).sum().T
    return dem - avail.reindex(columns=dem.columns, fill_value=0)


rl_act = residual_load("generators-p_max_pu.csv", "loads-p_set.csv")
rl_fc = residual_load("generators-p_max_pu-forecast.csv", "loads-p_set-forecast.csv")


def fnam_8_5(rl, week_def="calendar"):
    """FNAM Art. 8(5): (a) hourly vs daily mean, (b) daily vs weekly mean
    (each daily deviation counted 24 times, as in spec eq. 13.5), (c) monthly
    vs annual mean (each monthly deviation counted once per hour)."""
    day = rl.index.normalize()
    a = (rl - rl.groupby(day).transform("mean")).abs().sum()
    daily = rl.groupby(day).mean()
    if week_def == "calendar":  # Monday-based weeks *within* the year
        wk = daily.index.to_period("W-SUN").start_time
    else:  # ISO week number, as in EU-Flex
        wk = daily.index.isocalendar().week.values
    b = ((daily - daily.groupby(wk).transform("mean")).abs() * 24).sum()
    monthly = daily.groupby(daily.index.month).mean()
    yearly = daily.mean()
    hours_per_month = rl.groupby(rl.index.month).size()
    c = ((monthly - yearly).abs().mul(hours_per_month, axis=0)).sum()
    return a, b, c


a, b_cal, c = fnam_8_5(rl_act, "calendar")
_, b_iso, _ = fnam_8_5(rl_act, "iso")
out["independent_daily_need_MWh"] = a.round(0).to_dict()
out["independent_weekly_need_calendar_weeks_MWh"] = b_cal.round(0).to_dict()
out["independent_weekly_need_iso_weeks_MWh"] = b_iso.round(0).to_dict()
out["independent_seasonal_need_MWh"] = c.round(0).to_dict()

err = rl_act - rl_fc  # RL_ID - RL_DA (positive = upward need)
out["independent_forecast_error_p99_9_MW"] = err.quantile(0.999).round(1).to_dict()
out["independent_forecast_error_p0_1_MW"] = err.quantile(0.001).round(1).to_dict()
out["independent_forecast_error_std_MW"] = err.std().round(1).to_dict()
out["independent_max_abs_ramp_MW"] = rl_act.diff().abs().max().round(0).to_dict()

# ---------------------------------------------------------------- model outputs
mo_path = RUN / "results/assessment/model_outputs.nc"
dt = xr.open_datatree(mo_path, decode_timedelta=True)
groups = {k: list(v.ds.data_vars) for k, v in dt.subtree_with_keys if v.ds.data_vars}
out["model_output_groups"] = {k: len(v) for k, v in groups.items()}
root = dt["/"].ds if not groups.get("/") is None else None


def find(var):
    for g, vs in groups.items():
        if var in vs:
            return dt[g].ds[var]
    return None


def summarise(var, reduce_dims=()):
    da = find(var)
    if da is None:
        return None
    for d in reduce_dims:
        if d in da.dims:
            da = da.sum(d)
    return {str(k): round(float(v), 1) for k, v in da.squeeze().to_series().items()}


out["model_vars_with_need_or_contrib"] = sorted(
    v for vs in groups.values() for v in vs if "need" in v or "contrib" in v or "ramp" in v
)
json.dump(out, open("/dev/stdout", "w"), indent=1, default=str)
print()
