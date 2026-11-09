"""
Short-term-need experiments (findings F-08 and F-09).

1. --noise RUNDIR: base networks built with forecast_timeseries_source: noise
   (default of the model). Reports cross-zone correlation of the synthetic
   load errors, load/wind error correlation, and the resulting percentiles.
2. --proba RUNDIR: on a solved teaser run, calls the model's own probabilistic
   short-term functions and recomputes the uncovered hours after adding the
   storage / implicit-DSR power headroom the model leaves out.

Usage:
    python adversarial_review/scripts/analyse_short_term.py --noise runs/adv_noise
    python adversarial_review/scripts/analyse_short_term.py --proba runs/teaser
"""

import logging
import sys

import pypsa
import yaml

logging.disable(logging.WARNING)
mode, run = sys.argv[1], sys.argv[2]

if mode == "--noise":
    nets = f"{run}/resources/networks/base_network_2030_2013_"
    fc = pypsa.Network(nets + "forecast_0.nc")
    ac = pypsa.Network(nets + "actual_0.nc")
    rel = fc.loads_t.p_set / ac.loads_t.p_set - 1
    print("relative load error correlation between zones\n", rel.corr().round(4))
    w = [c for c in fc.generators_t.p_max_pu if "Wind" in c]
    werr = fc.generators_t.p_max_pu[w] - ac.generators_t.p_max_pu[w]
    print("corr(load err N1, wind err N1) =", round(rel.iloc[:, 0].corr(werr.iloc[:, 0]), 3))
    res = [c for c in fc.generators_t.p_max_pu if "Solar" in c or "Wind" in c]

    def rl(n):
        avail = n.generators_t.p_max_pu[res].mul(n.generators.p_nom[res])
        avail = avail.T.groupby(n.generators.bus[res]).sum().T
        return n.loads_t.p_set.T.groupby(n.loads.bus).sum().T - avail

    e = rl(ac) - rl(fc)
    print("P99.9", e.quantile(0.999).round(0).to_dict())
    print("P0.1 ", e.quantile(0.001).round(0).to_dict())

elif mode == "--proba":
    from euflex.eu_flex_model.scripts import calculate_model_outputs as cmo

    cfg = yaml.safe_load(open("src/euflex/eu_flex_model/config/config.default.yaml"))
    res = cfg["eva"]["base_network"]["renewable_carriers"]
    da = pypsa.Network(f"{run}/results/networks/day_ahead_network_2030_2013.nc")
    idn = pypsa.Network(f"{run}/results/networks/intraday_network_2030_2013.nc")
    dist = cmo.compute_forecast_error_distribution([(idn, da)], cfg, res)
    r = cmo.calculate_probabilistic_short_term_requirements(idn, da, dist, cfg, res)
    up = r["uncovered_need_up"].to_pandas()
    dn = r["uncovered_need_down"].to_pandas()
    print("model: uncovered hours up  ", (up > 1).sum().to_dict())
    print("model: uncovered hours down", (dn > 1).sum().to_dict())
    su, p = da.storage_units, da.storage_units_t.p
    hu = (su.p_nom * su.p_max_pu - p).clip(lower=0).T.groupby(su.bus).sum().T
    hd = (p - su.p_nom * su.p_min_pu).clip(lower=0).T.groupby(su.bus).sum().T
    hu.index, hd.index = up.index, dn.index
    up2 = (up - hu.reindex(columns=up.columns, fill_value=0)).clip(lower=0)
    dn2 = (dn - hd.reindex(columns=dn.columns, fill_value=0)).clip(lower=0)
    print("+storage/iDSR power headroom: up  ", (up2 > 1).sum().to_dict())
    print("+storage/iDSR power headroom: down", (dn2 > 1).sum().to_dict())
    shed = idn.generators_t.p.filter(like="shedding").sum().round(0)
    print("load shedding actually simulated in ID (MWh):", shed.to_dict())
