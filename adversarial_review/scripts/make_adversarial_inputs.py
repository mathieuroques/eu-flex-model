"""
Build the corrupted / edge-case input datasets used in the adversarial review.

Each dataset is a copy of data/teaser/ty_2030_cy_2013 with one family of
defects injected. Feed them to the model with a copy of config/teaser.yaml
whose sensitivity_path and forecast_*_path point at the dataset, and build
only the base networks, e.g.:

    snakemake -c1 --configfile <cfg> --directory runs/adv_M1 -- \
        resources/networks/base_network_2030_2013_forecast_0.nc \
        resources/networks/base_network_2030_2013_actual_0.nc

Usage: python adversarial_review/scripts/make_adversarial_inputs.py OUTDIR
"""

import os
import shutil
import sys

import numpy as np
import pandas as pd

OUT = sys.argv[1]
SRC = "data/teaser/ty_2030_cy_2013"


def make(name, fn, sub="ty_2030_cy_2013"):
    d = f"{OUT}/{name}/{sub}"
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(SRC, d)
    fn(d)


def m1(d):  # forecast load column missing
    f = d + "/loads-p_set-forecast.csv"
    pd.read_csv(f, index_col=0).drop(columns=["N3_load"]).to_csv(f)


def m2(d):  # NaN / >1 / <0 renewable availability
    f = d + "/generators-p_max_pu.csv"
    x = pd.read_csv(f, index_col=0)
    x.iloc[100:200, 0] = np.nan
    x.iloc[300:400, 1] = 1.5
    x.iloc[500:600, 2] = -0.3
    x.to_csv(f)


def m3(d):  # negative / NaN / absurd load
    f = d + "/loads-p_set.csv"
    x = pd.read_csv(f, index_col=0)
    x.iloc[1000:1010, 0] = -50000
    x.iloc[2000:2010, 1] = np.nan
    x.iloc[3000, 2] = 1e9
    x.to_csv(f)


def m4(d):  # forecasts shifted by 12 h (positional alignment)
    for f in ["/loads-p_set-forecast.csv", "/generators-p_max_pu-forecast.csv"]:
        x = pd.read_csv(d + f, index_col=0)
        y = x.copy()
        y.iloc[:] = np.roll(x.values, 12, axis=0)
        y.to_csv(d + f)


def m5(d):  # parameters the schema does reject
    g = pd.read_csv(d + "/generators.csv", index_col=0)
    g.loc["N1 Gas", "capital_cost"] = -30000
    g.loc["N2 Nuclear", "p_min_pu"] = 1.2
    g.to_csv(d + "/generators.csv")


def m6(d):  # parameters the schema does NOT reject
    g = pd.read_csv(d + "/generators.csv", index_col=0)
    g.loc["N1 Gas", "efficiency"] = 3.0
    g.loc["N1 Gas", "marginal_cost"] = -500
    g.loc["N2 Nuclear", "avg_forced_outage_rate"] = 1.7
    g.to_csv(d + "/generators.csv")
    lk = pd.read_csv(d + "/links.csv", index_col=0)
    lk.loc["N1-N2", "p_nom"] = -4000
    lk.to_csv(d + "/links.csv")


def leap_cy(d):  # climate year 2016 with 8784 hourly rows (Feb 29 = Feb 28)
    pos = np.r_[np.arange(0, 59 * 24), np.arange(58 * 24, 59 * 24), np.arange(59 * 24, 8760)]
    idx16 = pd.date_range("2016-01-01", "2016-12-31 23:00", freq="h")
    for f in os.listdir(d):
        if not f.endswith(".csv"):
            continue
        x = pd.read_csv(f"{d}/{f}", index_col=0)
        if f == "snapshots.csv":
            pd.DataFrame(
                {
                    "snapshot": idx16.strftime("%Y-%m-%d %H:%M:%S"),
                    "objective": 1.0,
                    "generators": 1.0,
                    "stores": 1.0,
                }
            ).to_csv(f"{d}/{f}")
        elif len(x) == 8760:
            if x.shape[1] == 0:
                y = pd.DataFrame(index=pd.RangeIndex(8784, name=x.index.name))
            else:
                y = x.iloc[pos].copy()
                y.index = pd.RangeIndex(8784, name=x.index.name)
            y.to_csv(f"{d}/{f}")


for name, fn in [
    ("M1_missing_forecast_load", m1),
    ("M2_aberrant_pmaxpu", m2),
    ("M3_aberrant_load", m3),
    ("M4_shifted_forecast", m4),
    ("M5_aberrant_params", m5),
    ("M6_unvalidated_params", m6),
]:
    make(name, fn)
make("leap", lambda d: None, sub="ty_2028_cy_2013")  # leap target year
make("leap", leap_cy, sub="ty_2030_cy_2016")  # leap climate year
print("written to", OUT)
