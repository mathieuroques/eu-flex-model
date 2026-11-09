# Draft response to ACER's public consultation on the preliminary EU-Flex model — Methodology

*Draft for an industrial stakeholder (generator / investor). Scope: the paper and the methodology (Modelling Specification v1.0), not code issues. Each point gives the concern, the evidence (reproducible, see `adversarial_review/`), and a concrete request. Deadline: 17 December 2026.*

*Reviewer notes in brackets [ ] must be removed before submission. Figures come from ACER's illustrative teaser case and show **sensitivities, not forecasts** (see §0.3).*

---

## 0. Summary

### 0.1 Why this matters to market participants

The EU-wide flexibility needs assessment is not an academic exercise. Under Regulation (EU) 2019/943 as amended:

- Art. 19e(7)(b): ACER assesses flexibility needs **at Union level** and their economically available potential.
- Art. 19f: Member States set **indicative national objectives** for non-fossil flexibility on the basis of the FNA reports.
- Art. 19g: Member States may introduce **support schemes paying for available capacity** of new demand response and storage when investment is insufficient.
- Art. 19h(a) and (f): such schemes must **"not go beyond what is necessary"** and must **"prevent undue distortions"** to price signals and market risk exposure.

EU-Flex results will be used to benchmark national reports and to frame recommendations. Methodological errors therefore translate directly into the size of out-of-market capacity payments and into the revenue outlook of every merchant flexible asset, existing or planned. **The standard of rigour should be proportionate to these economic consequences.**

### 0.2 Overall assessment

We support ACER's choices of an **open-source** tool, of a sequential day-ahead / intraday market simulation, and of an economic viability assessment (EVA) that reuses the dispatch simulation. These are sound foundations. On the latter point, EU-Flex improves on ERAA 2024, where ACER found a 1.7-4 h LOLE gap between the EVA (3 weather scenarios) and the dispatch (36).

However, in its present form the methodology does **not yet produce robust estimates of uncovered flexibility needs**. In our tests on ACER's teaser case, the deficit indicators are driven more by **modelling conventions** than by system physics:

| Convention changed (same physical system) | Effect observed on the teaser case |
|---|---|
| Unit-commitment representation (relaxed vs binary on aggregated fleets) | Energy not served ×30 ; battery NPV/MW ×23 ; nuclear NPV/MW −83 % |
| Scarcity price setting the EVA equilibrium (4 500 vs 10 000 €/MWh) | Adequacy level at "convergence" differs by a factor 2-3 (scarcity hours/yr) |
| Forecast-error source (synthetic default vs supplied forecasts) | P99.9 short-term need ×2.3 |
| Short-term method ("simulation" vs "probabilistic") | Uncovered short-term needs differ by more than three orders of magnitude |
| Any of the above | Descriptive "needs" (Art. 8(5) indicators) unchanged (0.0 %) |

Errors run in **both directions**: some choices inflate needs, others deflate them (§9). **Neither the sign nor the size of the net error is known today.** This is what market participants cannot accept as a basis for national objectives and support schemes.

### 0.3 Caveats on our evidence

The teaser is illustrative and not calibrated. Our magnitudes are therefore **orders of magnitude of sensitivity**, not estimates for the EU system. The direction of each effect is established by construction or by test. We address requests to the **final** model, and acknowledge that some points may already be under revision.

---

## 1. Economic viability assessment (EVA) and investment modelling

**1.1 Price-assumption sensitivity is a legal requirement and is missing.**
Art. 19e(2)(a) requires evaluating needs under "different assumptions in respect to electricity market prices". The EVA endogenously sets the adequacy level of the final fleet through scarcity pricing. In the teaser, load-shedding bids of 4 500 €/MWh sit below the configured day-ahead cap (5 000) and intraday cap (10 000), so the intraday cap never binds. For the teaser peaker, the "converged" band corresponds to 5.4-8.4 scarcity hours/yr at 4 500 €/MWh, but 2.4-3.7 h at 10 000 €/MWh.
→ **Request:** publish needs as a function of VoLL and price-cap assumptions, anchored to Member States' reliability standards (Art. 25, VoLL/CONE/RS methodology). Enforce consistency between shedding cost and price caps.

**1.2 Investor risk is not represented.**
The NPV is risk-neutral, with a single hurdle rate per asset. The ERAA methodology itself (ACER Decision 04/2026) requires mitigating investors' reaction to price spikes, by default through "partial discounting of Monte Carlo sample years with the highest revenues". EU-Flex has no such mechanism, so rare scarcity rents may be over-weighted.
→ **Request:** introduce explicit risk treatment (CVaR or ERAA-consistent discounting of high-revenue years), technology-specific and documented hurdle rates, and sensitivities.

**1.3 Revenue concentration and the revenue stack.** In the teaser, the peaker earns 95 % of its annual gross margin in 50 hours and explicit DSR 100 % in 10 hours, from a **single** climate year extrapolated over 20 years. Viability therefore rests on tail events that the methodology neither samples (one climate year) nor risk-weights.

**1.3b The revenue stack is incomplete for flexible assets.**
NPV includes day-ahead energy, intraday deviations and day-ahead reserve capacity. It excludes balancing energy and activation revenues, capacity mechanisms (only exogenous and disabled by default), forward hedging, support schemes and sub-hourly price shape (hourly model, while SDAC moved to 15-minute MTU on 1 October 2025). These omissions systematically understate the merchant value of batteries, demand response and fast thermal plants. The EVA then under-builds flexibility, which **inflates the "uncovered needs"** that could later justify Art. 19g payments.
→ **Request:** complete the revenue stack, or at least bound the omitted revenues with exogenous ranges, and publish asset-level revenue diagnostics by stream.

**1.4 Single-year profit extrapolated over the asset life.**
Profit per MW is interpolated between target years and **held constant from the last target year until decommissioning**, discounted from the first target year. With one target year and few climate years, two decades of cash flows rest on one market year. Teaser data also contain inconsistencies (new gas: lifetime 10 years, decommissioning year 2050).
→ **Request:** model revenue trajectories (cannibalisation, policy evolution) over several target years, include construction lead times and earliest-entry years, and validate lifetime/decommissioning consistency.

**1.5 The EVA equilibrium is ill-defined and its convergence is not reported.**
Fixed MW steps (default 800 MW for every asset and zone) can oscillate without converging. The convergence test can be blocked by assets saturated at their bounds, or wrongly declared "converged" when monotonicity constraints block an unprofitable asset. The status (e.g. "Aborted") is not reported in the published outputs.
In ACER's own EVA configuration (teaser-eva, with the documented temporal clustering) we observe the battery capacity jump from 100 to 3 100 MW and fall back to 245 MW within two iterations (NPV +410 → −900 → −532 k€/MW). At iteration 3 a day-ahead window becomes infeasible despite load shedding, and the whole EVA aborts under default settings. With the model's tolerant option (`fail_on_infeasibility: false`), 3 of the 12 representative weeks remain infeasible and 9 crash downstream: **the EVA cannot proceed beyond iteration 2 on ACER's EVA configuration.**
→ **Request:** use an equilibrium or co-optimisation formulation with guaranteed convergence, or adaptive steps, and publish convergence status, residual NPV and saturated assets with every result.

**1.6 Price formation.**
Unit commitment is relaxed on aggregated fleets, and prices are duals of an interior-point solution without crossover. The binary option offered in the manual as higher fidelity is invalid on aggregated fleets: it switches 30 GW on or off at once. In our test it changes NPV/MW by up to 23×.
→ **Request:** use clustered integer unit commitment (integer number of online units per cluster) or validate the relaxation against it, document the pricing rule (and uplift) and use vertex duals. Implement the HMMCP adjustment on **70 % of the prevailing cap** (not the initial cap), consistent with ACER Decision 01/2023 and 02/2026.

---

## 2. Definition of flexibility needs (what is measured)

**2.1 Separate description from deficit.**
The Art. 8(5) indicators (daily, weekly, seasonal) describe residual-load variability and are invariant to the flexibility supply. They cannot by themselves indicate a shortage. Only deficit indicators (uncovered needs, with probability, energy, frequency, duration) can support Art. 19f objectives.
→ **Request:** publish distinct indicator layers: variability, requirement envelopes per horizon (5 min to season), probabilistic deficits by cause, and marginal value of flexibility.

**2.2 The "simulation" short-term shortfall is a signed difference of two market outcomes.**
It mixes forecast bias with lack of flexibility. In the teaser it is +1 772 GWh in one zone and −1 072 GWh in another, and positive and negative values cancel in aggregates.
→ **Request:** use unsigned, cause-attributed deficits measured at the real-time stage.

**2.3 The "probabilistic" method omits flexibility the FNA methodology counts.**
FNAM Art. 10(2) counts margins of generation including renewables, storage, demand and exchange capacity. EU-Flex excludes storage, implicit DSR, renewables and interconnectors, and deducts FRR as well as FCR. In the teaser, a hydro-rich zone is "uncovered" 8 760 h/yr, versus at most a few hundred hours once storage power headroom alone is counted.
→ **Request:** align margins with FNAM 10(2)-(4), with state-of-charge constraints.

**2.4 Union-level and regional indicators are missing.**
On the teaser, regional needs are 70-82 % of the sum of zonal needs (P99.9: 74 %). Art. 19e(7)(b) asks for Union-level needs.
→ **Request:** publish zonal, regional (capacity calculation region) and Union-level indicators, and the realised cross-border pooling.

---

## 3. Attribution of contributions (technology neutrality)

The co-movement metric (spec. eq. 13.8) does not close on the need it decomposes: in the teaser, the sum of contributions equals 6 %, −19 % and 9 % of the daily need by zone, because variable renewables are counted twice. ACER's notebook fills the gap with a residual labelled "RES" or "Curtailment".

The metric also does not measure value. Implicit DSR receives about 2 % of the daily need, yet removing it multiplies energy not served by 4 and raises variable cost by about 0.41 bn€/yr in the teaser. Since Art. 19f objectives must specify the contributions of demand response and storage, and Art. 19e(4)(b)(i) requires considering "all available sources of flexibility in a cost-efficient manner", **attribution errors directly bias objectives between technologies and against existing assets**.

→ **Request:** publish (a) a closed accounting decomposition, including curtailment and shedding terms; (b) marginal (counterfactual) contributions per technology family; (c) Shapley-based allocations across families; and the contribution of **existing** flexible assets, including hydro and thermal plants.

---

## 4. Information structure and time resolution

**4.1 Intraday perfect foresight.**
The intraday stage solves 72-hour windows with the realised values known in advance, and FRR blocking uses the realised forecast error. Imbalances are therefore anticipated hours ahead, which biases short-term needs **downwards** by construction. In our test, shortening the intraday foresight from 72 h to 8 h (still perfect within the 8 h) raised short-term ENS shortfall by 22 % and the curtailment shortfall by 13-15 %. It also moved implicit-DSR contributions by −48 % to +136 % and made 1 % of intraday windows infeasible despite load shedding. This is a lower bound on the effect.
→ **Request:** sequential information revelation (forecast updates at intraday gates, balancing stage with ex-ante sized reserves), and publication of the value-of-information gap.

**4.2 Hourly resolution.**
SDAC, SIDC and balancing operate at 15 minutes, and FNAM Art. 10(1)(e) distinguishes very fast, fast and slow flexibility. Hourly modelling misses intra-hour ramps and cycling, as established in the literature (Deane et al., Applied Energy 2014), and undervalues fast assets.
→ **Request:** 15-minute market stages, plus a 5-minute or statistical layer for balancing.

---

## 5. Uncertainty: weather, forecast errors, outages

**5.1 Weather.**
Each climate year is simulated independently, January to December, with cyclic storage. Winter droughts spanning the turn of the year, the most demanding events for long-duration flexibility (e.g. 1996/97), are cut in two. State-of-the-art studies use 35-200 climate years, summer-to-summer or chained simulation, and climate projections: RTE (200 years, RCP4.5/8.5), Elia (200 synthetic years), Kittel, Roth & Schill.
→ **Request:** chained multi-year simulation, a large climate-consistent ensemble with explicit extreme-event stress tests, and published Monte Carlo convergence (ERAA's α(N) criterion).

**5.2 Forecast errors.**
The default is hard-coded synthetic noise, with fixed seeds, perfectly correlated across zones and artificially correlated between load and wind. FNAM Art. 10(1) requires extrapolating at least two years of historical errors, with conditional distributions and separation from forced outages. CAISO (conditional quantile regression) and Elia (convolution, dynamic dimensioning) show operational practice.
→ **Request:** empirically calibrated, conditional, spatially correlated error models projected to the target year with explicit forecast-improvement assumptions, and several realisations per climate year.

**5.3 Outages.**
→ **Request:** unit-level Monte Carlo with convergence criteria, separately reported from forecast errors.

---

## 6. Storage needs for RES integration ("dummy storage")

The dummy storage is lossless by construction, contrary to FNAM Art. 8(10), which requires "the most representative roundtrip efficiency for each" duration of 2-200 h. Its cost is identical for all durations. Its target applies year by year rather than as an average across weather years (FNAM Art. 8(12)(a)). Research shows that efficiency and energy-capacity cost are the decisive parameters (Sepulveda et al., Nature Energy 2021), and that multi-year optimisation materially changes long-duration needs (Ruhnau & Qvist 2022; Dowling et al., Joule 2020).
Adding efficiencies alone is **not** a fix. In our test (round-trip efficiencies of 0.85 / 0.60 / 0.35 for 4 / 50 / 200 h), the computed need **falls**: for 4 h at a 2 % target, from 97.5 GW to 22.4 GW. A 200-h store absorbs 10.5 TWh and returns only 3.7 TWh. Energy dissipated in storage counts as "integrated" RES, so the indicator rewards waste, acting as a dump load.
→ **Request:** redefine the target on RES energy **effectively consumed**, net of storage losses (cf. FNAM Art. 2(2)(bb), "effectively integrated"), then use technology-neutral storage classes with realistic efficiencies, multi-year chained optimisation, average-based targets, Pareto curves and sensitivities.

---

## 7. Hydro and storage valuation

Reservoirs follow a perfect-foresight annual plan, with minimum state-of-charge targets and no water value in price formation. The established practice in hydro-dominated systems is SDDP-based water values under inflow and weather uncertainty (e.g. SINTEF ProdRisk, PLEXOS medium-term). This matters for prices, and hence for the revenues of all competing flexible assets.
→ **Request:** stochastic water values, or at least sensitivity bounds.

---

## 8. Transparency, validation and process

The Modelling Specification (§5) foresees unit, regression and historical validation, including reproducing ERAA 2023. None of these results is published, and the model's own integration test suite fails on the teaser case.

→ **Requests:**
- (a) publish a validation dossier before the July 2027 report: backcasting of recent years at zonal level (prices, flows, dispatch, curtailment, balancing volumes) with acceptance criteria, and benchmarks against ERAA and at least one national FNA;
- (b) publish confidence intervals for all indicators (bootstrap or extreme-value methods for P99.9, which rests on about 9 hours per climate year);
- (c) run a global sensitivity analysis ranking the drivers of the results;
- (d) open a **second consultation** on the final model with a change log;
- (e) give stakeholders access to the input dataset, or a representative synthetic equivalent, to replicate results.

---

## 9. Direction of biases (why the net error is unknown)

| Choice | Likely direction on uncovered needs | Status |
|---|---|---|
| Probabilistic margins exclude storage, RES and interconnectors ; FRR deducted | ↑ overestimation | Measured (teaser) |
| Incomplete revenue stack for flexible assets → EVA under-builds flexibility | ↑ | By construction |
| Intraday perfect foresight | ↓ underestimation | Measured: +13-22 % on short-term deficits with 8 h foresight (lower bound) |
| Hourly resolution | ↓ for fast needs | Literature |
| Lossless dummy storage ; single, calendar-cut years | ↓ storage needs | By construction / literature |
| Perfect-foresight hydro plan | ↓ | By construction |
| Synthetic forecast errors | ↓ or ↑ (×2.3 in the teaser) | Measured |
| Unit-commitment convention ; price cap / VoLL in the EVA | ↕ (×30 ENS ; ×2-3 adequacy level) | Measured |

**Conclusion.** Before EU-Flex outputs inform national objectives or support schemes, ACER should publish the uncertainty ranges and sensitivity analyses above. A single number per zone, without ranges, would not satisfy Art. 19h(a) ("not go beyond what is necessary").

---

*Evidence and reproduction scripts: `adversarial_review/` (reports 02 and 04, reference 05, scripts and evidence folders). [Attach a short annex with the key tables before submission.]*
