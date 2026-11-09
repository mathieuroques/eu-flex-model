"""
Investor view: concentration of each flexible asset's gross margin in a few
hours of the (single) simulated climate year, on the day-ahead network.

Usage: python adversarial_review/scripts/revenue_concentration.py runs/teaser
"""

import logging
import sys

import numpy as np
import pandas as pd
import pypsa

logging.disable(logging.WARNING)
run = sys.argv[1]
da = pypsa.Network(f"{run}/results/networks/day_ahead_network_2030_2013.nc")
price = da.buses_t.marginal_price
rows = []
for comp, df, p in [("Generator", da.generators, da.generators_t.p),
                    ("StorageUnit", da.storage_units, da.storage_units_t.p)]:
    for a in df.index:
        if any(k in a for k in ["shedding", "spillage", "Solar", "Wind"]):
            continue
        pr = price[df.loc[a, "bus"]]
        mc = df.loc[a, "marginal_cost"] if "marginal_cost" in df else 0.0
        margin = (pr - mc) * p[a] if comp == "Generator" else pr * p[a]
        total = margin.sum()
        if total <= 0:
            continue
        s = margin.sort_values(ascending=False)
        rows.append({
            "asset": a,
            "gross margin MEUR": round(total / 1e6, 1),
            "share top 10 h": round(s.iloc[:10].sum() / total, 3),
            "share top 50 h": round(s.iloc[:50].sum() / total, 3),
            "share top 1 % h (88)": round(s.iloc[:88].sum() / total, 3),
            "share hours price>=3500": round(margin[pr >= 3500].sum() / total, 3),
        })
print(pd.DataFrame(rows).set_index("asset").to_string())
