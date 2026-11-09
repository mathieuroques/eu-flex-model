"""
Compare a variant run with the teaser baseline on the indicators that carry
the FNA conclusions (one modelling convention changed at a time).

Usage: python adversarial_review/scripts/compare_runs.py runs/teaser runs/<variant> [...]
"""

import logging
import sys

import pandas as pd
import pypsa
import xarray as xr

logging.disable(logging.WARNING)
pd.set_option("display.width", 220)


def load(run):
    ds = xr.open_datatree(f"{run}/results/assessment/model_outputs.nc")["base"].ds
    da = pypsa.Network(f"{run}/results/networks/day_ahead_network_2030_2013.nc")
    idn = pypsa.Network(f"{run}/results/networks/intraday_network_2030_2013.nc")
    return ds, da, idn


def z(ds, v, scale=1.0, reduce=()):
    d = ds[v].squeeze()
    for r in reduce:
        if r in d.dims:
            d = d.sum(r)
    return (d.to_series() / scale).round(2)


def summary(run):
    ds, da, idn = load(run)
    rows = {}
    rows["ENS ID (GWh)"] = z(ds, "total_energy_not_served", 1e3)
    rows["Écrêtement ID (TWh)"] = z(ds, "curtailment_aggregated", 1e6, reduce=("carrier",))
    rows["ST shortfall écrêtement (GWh, signé)"] = z(ds, "short_term_shortfall_curtailment_total", 1e3)
    rows["ST shortfall ENS (GWh)"] = z(ds, "short_term_shortfall_ens_total", 1e3)
    rows["Besoin journalier FNAM 8(5)(a) (TWh)"] = z(ds, "daily_flexibility_need_aggregated", 1e6)
    rows["P99.9 court terme (MW)"] = z(ds, "short_term_need_upward_p99_9")
    rows["Prix moyen DA (€/MWh)"] = da.buses_t.marginal_price.mean().round(1)
    rows["Prix moyen ID (€/MWh)"] = idn.buses_t.marginal_price.mean().round(1)
    rows["Heures prix DA ≥ 3500"] = (da.buses_t.marginal_price >= 3500).sum()
    gas = idn.generators_t.p.filter(like="Gas").sum() / 1e6
    rows["Gaz ID (TWh)"] = pd.Series({"N1": round(float(gas.sum()), 2)})
    starts = da.generators_t.status.diff().clip(lower=0).sum() if not da.generators_t.status.empty else pd.Series()
    rows["Démarrages équiv. DA (flotte)"] = starts.groupby(da.generators.bus).sum().round(1)
    obj = (idn.generators_t.p * idn.generators.marginal_cost).sum().sum() / 1e9
    rows["Coût variable ID (G€)"] = pd.Series({"total": round(float(obj), 3)})
    tc = ds["technology_contributions_daily"].squeeze().to_pandas()
    rows["Contrib. journalière Gaz (TWh)"] = (tc.loc["Gas"] / 1e6).round(2) if "Gas" in tc.index else pd.Series()
    rows["Contrib. journalière iDSR (TWh)"] = (tc.loc["DSR_implicit"] / 1e6).round(3) if "DSR_implicit" in tc.index else pd.Series()
    rows["Contrib. journalière Hydro (TWh)"] = (tc.loc["Hydro - Reservoir"] / 1e6).round(2) if "Hydro - Reservoir" in tc.index else pd.Series()
    flat = {}
    for metric, ser in rows.items():
        for zone, val in pd.Series(ser).items():
            flat[(metric, str(zone))] = float(val)
    return pd.Series(flat)


base = sys.argv[1]
out = {"baseline": summary(base)}
for r in sys.argv[2:]:
    out[r.split("/")[-1]] = summary(r)
df = pd.concat(out, axis=1).dropna(how="all")
for c in df.columns[1:]:
    df[f"Δ% {c}"] = ((df[c] - df["baseline"]) / df["baseline"].abs() * 100).round(1)
print(df.to_string())
