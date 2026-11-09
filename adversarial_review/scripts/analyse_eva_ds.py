"""
EVA trajectory and dummy-storage comparison.

  python adversarial_review/scripts/analyse_eva_ds.py --eva runs/eva_clustered
  python adversarial_review/scripts/analyse_eva_ds.py --ds runs/ds_base runs/ds_lossy
"""

import glob
import logging
import re
import sys

import pandas as pd
import pypsa

logging.disable(logging.WARNING)
pd.set_option("display.width", 220)
mode = sys.argv[1]

if mode == "--eva":
    run = sys.argv[2]
    rows = []
    for f in sorted(glob.glob(f"{run}/resources/convergence/convergence_*.txt"),
                    key=lambda p: int(re.findall(r"_(\d+)\.txt", p)[0])):
        it = int(re.findall(r"_(\d+)\.txt", f)[0])
        status = open(f).read().strip()
        cap = f"{run}/resources/capacities/capacity_{it}.csv"
        npv = f"{run}/resources/npv/npv_{it}.csv"
        row = {"it": it, "status": status}
        try:
            c = pd.read_csv(cap, index_col=[0, 1])
            c = pd.to_numeric(c.iloc[:, -1], errors="coerce")
            for k in ["N1 Gas", "N1 BESS"]:
                hit = [i for i in c.index if i[1] == k]
                if hit:
                    row[f"cap {k} (MW)"] = round(float(c.loc[hit[0]]), 0)
        except Exception as e:  # noqa: BLE001
            row["cap"] = f"n/a ({e.__class__.__name__})"
        try:
            v = pd.read_csv(npv, index_col=[0, 1])
            v = pd.to_numeric(v.iloc[:, -1], errors="coerce")
            for k in ["N1 Gas", "N1 BESS"]:
                hit = [i for i in v.index if i[1] == k]
                if hit:
                    row[f"NPV {k} (kEUR/MW)"] = round(float(v.loc[hit[0]]) / 1e3, 1)
        except Exception:  # noqa: BLE001
            pass
        rows.append(row)
    print(pd.DataFrame(rows).to_string(index=False))

elif mode == "--ds":
    out = {}
    for run in sys.argv[2:]:
        name = run.rstrip("/").split("/")[-1]
        res = {}
        for f in glob.glob(f"{run}/results/assessment/dummy_storage_optimization/network_*.nc"):
            mh, ct = re.findall(r"_(\d+)_(ct\d+)\.nc$", f)[0]
            n = pypsa.Network(f)
            d = n.storage_units.index[n.storage_units.carrier == "Dummy Storage"]
            p = float(n.storage_units.loc[d, "p_nom_opt"].sum())
            e = float((n.storage_units.loc[d, "p_nom_opt"] * n.storage_units.loc[d, "max_hours"]).sum())
            eff = float(n.storage_units.loc[d, "efficiency_dispatch"].mean() ** 2)
            spill = n.generators_t.p.filter(like="spillage").sum().sum() if not n.generators_t.p.empty else 0.0
            res[(int(mh), ct)] = {"GW": round(p / 1e3, 2), "TWh": round(e / 1e6, 3),
                                  "RTE": round(eff, 2), "spill_GWh": round(-float(spill) / 1e3, 1)}
        out[name] = pd.DataFrame(res).T.sort_index()
    df = pd.concat(out, axis=1)
    print(df.to_string())
