"""
Cheap methodological robustness experiments on the teaser case (no solver).

M-A  Sampling uncertainty of the FNAM Art. 10 percentiles (P99.9 / P0.1)
     estimated from one climate year (8 760 values), by moving-block bootstrap
     (daily blocks, to respect autocorrelation), compared with P99 / P1.
M-B  Indeterminacy of the EVA equilibrium implied by the NPV convergence
     band (+/- threshold), translated into scarcity hours (LOLE-like) for the
     teaser gas peaker, using the model's own discounting convention.
M-C  Cross-border diversification: sum of zonal needs vs. need of the
     aggregated (copper-plate) region, for the FNAM 8(5) indicators and the
     short-term percentiles. EU-Flex only reports zonal values.

Usage: python adversarial_review/scripts/method_experiments.py
"""

import numpy as np
import pandas as pd

DATA = "data/teaser/ty_2030_cy_2013"
RES = ["Solar (PV)", "Wind Onshore", "Wind Offshore", "Hydro - Run of River (Turbine)"]
gens = pd.read_csv(f"{DATA}/generators.csv", index_col=0)
loads = pd.read_csv(f"{DATA}/loads.csv", index_col=0)
idx = pd.date_range("2030-01-01", periods=8760, freq="h")


def rl(pu_file, load_file):
    pu = pd.read_csv(f"{DATA}/{pu_file}", index_col=0).set_axis(idx)
    ld = pd.read_csv(f"{DATA}/{load_file}", index_col=0).set_axis(idx)
    r = [g for g in pu if gens.loc[g, "carrier"] in RES]
    av = pu[r].mul(gens.loc[r, "p_nom"]).T.groupby(gens.loc[r, "bus"]).sum().T
    return ld.T.groupby(loads.loc[ld.columns, "bus"]).sum().T - av


rl_a = rl("generators-p_max_pu.csv", "loads-p_set.csv")
rl_f = rl("generators-p_max_pu-forecast.csv", "loads-p_set-forecast.csv")
err = rl_a - rl_f

# ---------------------------------------------------------------- M-A
print("=== M-A  Bootstrap (365 daily blocks, 2000 resamples) of short-term percentiles")
rng = np.random.default_rng(0)
days = err.index.normalize()
blocks = [err.loc[days == d].to_numpy() for d in days.unique()]
B = 2000
stats = {q: [] for q in (0.999, 0.99, 0.001, 0.01)}
for _ in range(B):
    pick = rng.integers(0, len(blocks), len(blocks))
    sample = np.vstack([blocks[i] for i in pick])
    for q in stats:
        stats[q].append(np.quantile(sample, q, axis=0))
for q, vals in stats.items():
    v = np.array(vals)
    point = err.quantile(q).to_numpy()
    lo, hi = np.percentile(v, [5, 95], axis=0)
    width = (hi - lo) / np.abs(point) * 100
    print(f"P{q*100:g}: " + ", ".join(
        f"{z}: {p:,.0f} MW [90% CI {a:,.0f} .. {b:,.0f}] (+/-{w/2:.0f}%)"
        for z, p, a, b, w in zip(err.columns, point, lo, hi, width)))
n_tail = int(round(8760 * 0.001))
print(f"Values beyond P99.9 in one climate year: ~{n_tail} hours")

# ---------------------------------------------------------------- M-B
print("\n=== M-B  EVA equilibrium band implied by the NPV threshold (teaser N1 Gas)")
g = gens.loc["N1 Gas"]
capex = g["capital_cost"]           # EUR/MW/yr, annualised (PyPSA convention)
mc = g["marginal_cost"]
r = g["hurdle_rate"]
ty, decom = 2030, int(g["decommissioning_year"])
annuity = sum(1 / (1 + r) ** k for k in range(0, decom - ty + 1))
for scarcity_price, label in [(4500, "teaser shedding bid"), (5000, "DA cap"), (10000, "ID cap")]:
    rent = scarcity_price - mc
    for thr in (70_000, 20_000):
        band = thr / annuity          # EUR/MW/yr of annual profit
        h_lo = (capex - band) / rent
        h_hi = (capex + band) / rent
        print(f"threshold {thr:>6,} EUR/MW, scarcity price {scarcity_price:>6} ({label}): "
              f"'converged' for {h_lo:4.1f} .. {h_hi:4.1f} scarcity hours/yr "
              f"(ratio {h_hi/h_lo:.2f})")
print(f"(annuity factor {annuity:.2f} over {ty}-{decom} at {r:.0%}; capex {capex:,.0f} EUR/MW/yr; "
      "peaker earns only in scarcity hours, inframarginal rents ignored)")

# ---------------------------------------------------------------- M-C
print("\n=== M-C  Diversification: sum of zonal needs vs. need of the aggregated region")


def needs(s):
    d = s.index.normalize()
    hourly = (s - s.groupby(d).transform("mean")).abs().sum()
    daily = s.groupby(d).mean()
    wk = daily.index.to_period("W-SUN").start_time
    weekly = ((daily - daily.groupby(wk).transform("mean")).abs() * 24).sum()
    m = daily.groupby(daily.index.month).mean()
    seas = ((m - daily.mean()).abs() * s.groupby(s.index.month).size()).sum()
    return pd.Series({"FNAM 8(5)(a) hourly": hourly, "FNAM 8(5)(b) daily": weekly,
                      "FNAM 8(5)(c) seasonal": seas})


zonal = sum(needs(rl_a[z]) for z in rl_a)
agg = needs(rl_a.sum(axis=1))
tab = pd.DataFrame({"sum of zones (TWh)": zonal / 1e6, "region (TWh)": agg / 1e6})
tab["region / sum"] = agg / zonal
print(tab.round(3).to_string())
print("P99.9 short-term: sum of zones {:,.0f} MW, region {:,.0f} MW (ratio {:.2f})".format(
    err.quantile(0.999).sum(), err.sum(axis=1).quantile(0.999),
    err.sum(axis=1).quantile(0.999) / err.quantile(0.999).sum()))
print("max |ramp|: sum of zones {:,.0f} MW, region {:,.0f} MW".format(
    rl_a.diff().abs().max().sum(), rl_a.sum(axis=1).diff().abs().max()))
