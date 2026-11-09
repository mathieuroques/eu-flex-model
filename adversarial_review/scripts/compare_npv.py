"""
Investor view: NPV per MW (EUR/MW, as computed by the model's EVA) of each
asset under the different modelling conventions, and the resulting viability
verdict against the EVA threshold.

Usage: python adversarial_review/scripts/compare_npv.py runs/teaser runs/<variant> ...
"""

import sys

import pandas as pd

pd.set_option("display.width", 250)
THRESHOLD = 70_000  # default eva.capacity_update.threshold (EUR/MW)

cols = {}
details = {}
for run in sys.argv[1:]:
    name = run.rstrip("/").split("/")[-1]
    npv = pd.read_csv(f"{run}/resources/npv/npv_0.csv", index_col=[0, 1])
    cols[name] = pd.to_numeric(npv.iloc[:, -1], errors="coerce")
    log = pd.read_csv(f"{run}/resources/npv/npv_computation_log_0.csv")
    log = log.set_index(["component", "name"])
    details[name] = log
df = pd.DataFrame(cols)
keep = ~df.index.get_level_values("name").str.contains("shedding|spillage")
df = df[keep]
print("NPV per MW (kEUR/MW), first target year")
print((df / 1e3).round(0).to_string())


def verdict(v):
    if pd.isna(v):
        return "n/a"
    return "viable(+)" if v > THRESHOLD else ("non-viable(-)" if v < -THRESHOLD else "in band")


print("\nEVA verdict at +/-70 kEUR/MW")
print(df.apply(lambda c: c.map(verdict)).to_string())
base = df.columns[0]
flips = (df.apply(lambda c: c.map(verdict)).ne(df[base].map(verdict), axis=0)).sum()
print("\nNumber of assets whose verdict differs from", base, ":", flips.to_dict())

# revenue decomposition for selected assets
sel = [n for n in df.index.get_level_values("name") if any(k in n for k in ["Gas", "BESS", "Nuclear", "Hydro", "iDSR"])]
rows = []
for name, log in details.items():
    for a in sel:
        hits = [i for i in log.index if i[1] == a]
        if not hits:
            continue
        r = log.loc[hits[0]]
        e_da = r.filter(like="energy_revenue_da").sum()
        e_id = r.filter(like="energy_revenue_id").sum()
        res = r.filter(like="reserves_revenue").sum()
        opex = r.filter(like="opex").sum()
        capex = r.filter(like="capex_annualized").sum()
        rows.append({"run": name, "asset": a, "DA energy MEUR": e_da / 1e6, "ID energy MEUR": e_id / 1e6,
                     "reserves MEUR": res / 1e6, "opex MEUR": opex / 1e6, "capex MEUR": capex / 1e6})
if rows:
    print("\nAnnual revenue stack (MEUR/yr) for selected assets")
    print(pd.DataFrame(rows).set_index(["asset", "run"]).sort_index().round(1).to_string())
