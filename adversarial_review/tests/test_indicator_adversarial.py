"""
Adversarial unit tests of the EU-Flex flexibility-indicator functions.

Each test builds a tiny synthetic PyPSA network whose "true" indicator value is
known analytically, then calls the production functions of
``euflex.eu_flex_model.scripts.calculate_model_outputs`` and checks the result.

Run (from the repository root, in an environment with the model installed):

    python -m pytest adversarial_review/tests/test_indicator_adversarial.py -v

A FAILING test documents a defect of the model (see the review report, the
finding id is in each test's docstring). A PASSING test documents a behaviour
that was challenged and held.
"""

import warnings

import numpy as np
import pandas as pd
import pypsa
import pytest

from euflex.eu_flex_model.scripts import calculate_model_outputs as cmo

warnings.filterwarnings("ignore")

# update_capacity.py does `from snakemake.script import snakemake` at module
# level, so it cannot be imported outside a Snakemake job (itself a
# testability defect, see F-17). Inject a placeholder so that its pure
# functions can be tested.
import snakemake.script as _ss  # noqa: E402

if not hasattr(_ss, "snakemake"):
    _ss.snakemake = None

RES = ["Solar (PV)", "Wind Onshore"]


def make_network(
    year=2013,
    ty=2030,
    load=None,
    solar_pu=None,
    name="net",
    hours=None,
):
    """One-bus network: load, solar, gas. Dispatch is set by hand (not solved)."""
    if hours is None:
        snapshots = pd.date_range(f"{year}-01-01", f"{year}-12-31 23:00", freq="h")
    else:
        snapshots = hours
    snapshots = snapshots.rename("snapshot")
    n = pypsa.Network()
    n.name = name
    n.set_snapshots(snapshots)
    n.add("Bus", "Z1")
    n.add("Carrier", ["Solar (PV)", "Gas", "load"])
    if load is None:
        load = pd.Series(1000.0, index=snapshots)
    if solar_pu is None:
        solar_pu = pd.Series(0.0, index=snapshots)
    n.add("Load", "Z1 load", bus="Z1", carrier="load", p_set=load)
    n.add(
        "Generator",
        "Z1 Solar (PV)",
        bus="Z1",
        carrier="Solar (PV)",
        p_nom=1000.0,
        p_max_pu=solar_pu,
    )
    n.add("Generator", "Z1 Gas", bus="Z1", carrier="Gas", p_nom=5000.0)
    # Hand-made "dispatch": solar fully used, gas covers the rest.
    solar_p = solar_pu * 1000.0
    n.generators_t.p = pd.DataFrame(
        {"Z1 Solar (PV)": solar_p, "Z1 Gas": load - solar_p}, index=snapshots
    )
    n.loads_t.p = pd.DataFrame({"Z1 load": load}, index=snapshots)
    n.meta = {"wildcards": {"ty": str(ty), "cy": str(year)}}
    return n


# --------------------------------------------------------------------------
# F-01: residual-load cache ignores time series -> DA/ID networks collide
# --------------------------------------------------------------------------
def test_F01_residual_load_cache_ignores_timeseries():
    """F-01. Two networks that differ ONLY in their load time series must give
    different residual loads. network_cache hashes static tables only."""
    snaps = pd.date_range("2013-01-01", periods=48, freq="h")
    n_da = make_network(hours=snaps, load=pd.Series(1000.0, index=snaps), name="x")
    n_id = make_network(hours=snaps, load=pd.Series(1500.0, index=snaps), name="x")
    rl_da = cmo.calculate_residual_load(n_da, RES)
    rl_id = cmo.calculate_residual_load(n_id, RES)
    assert float(rl_da.mean()) == pytest.approx(1000.0)
    # Expected 1500: the ID load. A cache collision returns 1000.
    assert float(rl_id.mean()) == pytest.approx(1500.0), (
        "calculate_residual_load returned the cached DA result for the ID network"
    )


def test_F01_short_term_need_zero_on_collision():
    """F-01 consequence: forecast error RL_ID - RL_DA collapses to zero."""
    snaps = pd.date_range("2013-01-01", periods=48, freq="h")
    n_da = make_network(hours=snaps, load=pd.Series(1000.0, index=snaps), name="y")
    n_id = make_network(hours=snaps, load=pd.Series(1200.0, index=snaps), name="y")
    dev = cmo.calculate_short_term_need_deviations(n_id, n_da, RES)
    assert float(dev["hourly"].mean()) == pytest.approx(200.0)


# --------------------------------------------------------------------------
# F-02: ISO week numbers merge the last days of December with week 1
# --------------------------------------------------------------------------
def test_F02_iso_week_merges_december_into_week1():
    """F-02. Residual load flat at 1000 MW all year except 30-31 Dec (target
    year 2030) where it is 3000 MW. Every calendar week is internally flat
    except the one containing 30-31 Dec, so the weekly need of week 1
    (1-6 January 2030) must be 0. ISO week grouping puts 30-31 Dec 2030 in
    ISO week 1 together with 1-6 Jan 2030."""
    snaps = pd.date_range("2013-01-01", "2013-12-31 23:00", freq="h")
    load = pd.Series(1000.0, index=snaps)
    load[snaps >= "2013-12-30"] = 3000.0
    n = make_network(load=load, name="iso")
    fn = cmo.calculate_flexibility_needs(n, RES)
    weekly = fn["weekly"].squeeze()
    week1 = float(weekly.sel(week=1).sum())
    assert week1 == pytest.approx(0.0, abs=1e-6), (
        f"Weekly need of ISO week 1 = {week1:,.0f} MWh although 1-6 January "
        "is perfectly flat: 30-31 December was pooled into week 1"
    )


# --------------------------------------------------------------------------
# F-03: contributions do not close on the need they claim to decompose
# --------------------------------------------------------------------------
def test_F03_contributions_sum_to_need():
    """F-03. Single zone, no interconnector, no curtailment, gas follows the
    residual load exactly. The only resource providing flexibility is gas, so
    the sum of contributions must equal the daily need, and solar (whose
    variability is already netted out of the residual load) must not appear
    with a non-zero contribution."""
    snaps = pd.date_range("2013-01-01", "2013-12-31 23:00", freq="h")
    hour = snaps.hour
    solar_pu = pd.Series(np.clip(np.sin((hour - 6) / 12 * np.pi), 0, None), index=snaps)
    load = pd.Series(1000.0 + 200.0 * np.cos(hour / 24 * 2 * np.pi), index=snaps)
    n = make_network(load=load, solar_pu=solar_pu, name="contrib")
    need = float(cmo.calculate_flexibility_needs(n, RES)["daily"].sum())
    contrib = cmo.calculate_technology_contributions(n, RES)["daily"].squeeze()
    by_carrier = contrib.to_series().groupby(level=0).sum()
    total = float(by_carrier.sum())
    print("need", need, "contributions", by_carrier.to_dict())
    assert by_carrier.get("Gas", 0) == pytest.approx(need, rel=1e-6)
    assert total == pytest.approx(need, rel=1e-3), (
        f"Sum of contributions {total:,.0f} MWh != daily need {need:,.0f} MWh "
        f"(solar counted as {by_carrier.get('Solar (PV)', 0):,.0f} MWh)"
    )


# --------------------------------------------------------------------------
# F-04: maximum ramping requirement reported in MWh
# --------------------------------------------------------------------------
def test_F04_max_ramp_units():
    """F-04. A ramp (MW/h step between consecutive MTUs) is a power, not an
    energy; the spec (Metrics table) and FNA Art. 9 express it in MW."""
    n = make_network(name="ramp")
    mr = cmo.calculate_maximum_ramping_requirement(n, RES)
    assert mr.attrs["units"] in ("MW", "MW/h"), f"units = {mr.attrs['units']}"


# --------------------------------------------------------------------------
# F-05: leap climate year cannot be mapped onto a non-leap target year
# --------------------------------------------------------------------------
def test_F05_leap_climate_year_crash():
    """F-05. ERAA/PECD climate years include leap years (1984, 1988, ...,
    2016). Snapshots that still contain 29 February crash the output stage."""
    snaps = pd.date_range("2016-02-28", "2016-03-01 23:00", freq="h")
    n = make_network(year=2016, hours=snaps, name="leap")
    cmo.calculate_residual_load(n, RES)  # raises ValueError if not handled


def test_F05b_leap_target_year_hour_index_gap():
    """F-05b. With a leap TARGET year (2028 is one of the spec's default target
    years) the hour-of-year coordinate skips 24 values after 28 February and
    runs to 8784, so per-hour arrays of different target years misalign."""
    n = make_network(year=2013, ty=2028, name="leapty")
    rl = cmo.calculate_residual_load(n, RES)
    hours = rl.hour.values
    assert hours.max() == 8760 and np.all(np.diff(hours) == 1), (
        f"hour-of-year runs to {hours.max()} with gaps: {sorted(set(np.diff(hours)))}"
    )


# --------------------------------------------------------------------------
# F-10: HMMCP price-cap update only rewrites prices exactly equal to the cap
# --------------------------------------------------------------------------
def test_F10_price_cap_update_ignores_scarcity_prices_not_equal_to_cap():
    """F-10. In the teaser data the load-shedding generators bid 4500/4510/4520
    EUR/MWh while the configured DA cap is 5000. Scarcity prices (4510) trigger
    HMMCP events (>= 70 % of 5000) but update_price_cap() only overwrites
    prices that are within 0.01 EUR of the starting cap, so the raised cap is
    never applied to any price: scarcity rents seen by the EVA stay at 4510."""
    from euflex.eu_flex_model.scripts.update_price_cap import update_price_cap

    snaps = pd.date_range("2030-01-01", periods=24 * 60, freq="h").rename("snapshot")
    n = pypsa.Network()
    n.set_snapshots(snaps)
    n.add("Bus", ["N1", "N2"])
    prices = pd.DataFrame(100.0, index=snaps, columns=["N1", "N2"])
    # Scarcity on 4 different days within 30 days, cleared at the shedding bid
    for day in (1, 3, 5, 40):
        prices.iloc[day * 24 + 18, 1] = 4510.0
    n.buses_t["marginal_price"] = prices.copy()
    final_cap, events, cap_ts = update_price_cap(n, 5000.0, 5000.0, 500.0, 20000.0)
    after = n.buses_t["marginal_price"]
    assert events >= 1 and final_cap > 5000.0  # the cap did rise
    scarcity_after = after.where(prices == 4510.0).stack()
    # Expected: scarcity prices after the transition period lifted to the new
    # cap (ex-post rescaling, which is what the routine is for).
    assert (scarcity_after > 4510.0).any(), (
        f"Cap rose to {final_cap} after {events} event(s) but no scarcity "
        "price was updated: they are only rewritten when equal to 5000"
    )


# --------------------------------------------------------------------------
# F-11: EVA convergence criterion can be blocked or spuriously satisfied
# --------------------------------------------------------------------------
def _eva_inputs(caps, pmax, pmin, ext=True, tys=(2030,)):

    idx = pd.MultiIndex.from_tuples([("Generator", "G")], names=["component", "name"])
    cols = list(tys)
    mk = lambda v: pd.DataFrame([v], index=idx, columns=cols, dtype=float)  # noqa: E731
    return dict(
        capacities=mk(caps),
        p_nom_max=mk(pmax),
        p_nom_min=mk(pmin),
        is_extendable=pd.Series([ext], index=idx),
        is_decommissionable=pd.Series([not ext], index=idx),
        ignore_monotonicity=pd.DataFrame(False, index=idx, columns=cols),
    )


def test_F11a_asset_at_bound_blocks_convergence_forever():
    """F-11a. A very profitable asset already at p_nom_max cannot grow; its
    capacity does not change, yet its NPV still feeds max_abs_npv, so the EVA
    can never report convergence (it runs to max_it and the indicators are
    then computed on a non-converged system, without any flag in the output)."""
    from euflex.eu_flex_model.scripts.update_capacity import update_capacities

    kw = _eva_inputs([1000.0], [1000.0], [0.0])
    npv = pd.DataFrame([[5e6]], index=kw["capacities"].index, columns=["2030"])
    upd, max_abs_npv, _ = update_capacities(npv=npv, threshold=70000, increment=800, **kw)
    assert float(upd.iloc[0, 0]) == 1000.0  # nothing can change
    assert max_abs_npv <= 70000, (
        f"max_abs_npv = {max_abs_npv:,.0f} > threshold although no capacity can "
        "move: convergence is unreachable"
    )


def test_F11b_blocked_unprofitable_asset_reported_converged():
    """F-11b. Converse case: an extendable asset with NPV = -1 MEUR/MW in the
    second target year is blocked by the monotonicity floor; the update
    returns delta 0 and the NPV is ignored, so the EVA reports 'Converged'
    while the asset is deeply unprofitable."""
    from euflex.eu_flex_model.scripts.update_capacity import update_capacities

    kw = _eva_inputs([1000.0, 1000.0], [1e5, 1e5], [0.0, 0.0], tys=(2030, 2035))
    npv = pd.DataFrame(
        [[0.0, -1e6]], index=kw["capacities"].index, columns=["2030", "2035"]
    )
    upd, max_abs_npv, _ = update_capacities(npv=npv, threshold=70000, increment=800, **kw)
    converged = max_abs_npv <= 70000
    assert not converged, (
        "EVA would declare convergence with an asset at NPV = -1,000,000 EUR/MW"
    )


def test_F11c_fixed_step_oscillation():
    """F-11c. Toy market: NPV/MW decreases linearly with capacity,
    NPV(c) = 300 kEUR - 0.5 kEUR/MW * c, zero at c* = 600 MW. With the
    default step of 800 MW and threshold of 70 kEUR/MW (band of +/-140 MW
    around c*), the fixed-step update never lands in the band: it cycles."""
    from euflex.eu_flex_model.scripts.update_capacity import update_capacities

    cap = 0.0
    trajectory = []
    for _ in range(12):
        kw = _eva_inputs([cap], [1e5], [0.0])
        npv_val = 300_000 - 500 * cap
        npv = pd.DataFrame([[npv_val]], index=kw["capacities"].index, columns=["2030"])
        upd, max_abs_npv, _ = update_capacities(
            npv=npv, threshold=70000, increment=800, **kw
        )
        trajectory.append((cap, npv_val, max_abs_npv <= 70000))
        cap = float(upd.iloc[0, 0])
    print(trajectory)
    assert any(conv for *_, conv in trajectory), f"never converges: {trajectory}"
