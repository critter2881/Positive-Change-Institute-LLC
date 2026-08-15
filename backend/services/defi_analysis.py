"""
PCI Sovereign DeFi Architecture analysis service.
"""

from __future__ import annotations


def invariant_xyk(reserve0: float, reserve1: float) -> float:
    """Return the constant-product invariant."""
    return reserve0 * reserve1


def price_impact(amount_in: float, reserve_in: float, reserve_out: float) -> float:
    """Return a simple constant-product price impact estimate."""
    del reserve_out  # reserved for future model expansion
    if reserve_in < 0 or amount_in < 0:
        raise ValueError("amount_in and reserve_in must be non-negative")
    denominator = reserve_in + amount_in
    return 0.0 if denominator == 0 else amount_in / denominator


def score_resilience(structure: dict) -> int:
    """Return a capped resilience score."""
    score = 0
    if structure.get("invariant_stability") == "high":
        score += 30
    if structure.get("volatility_exposure") == "low":
        score += 20
    if structure.get("liquidity_depth") == "high":
        score += 30
    if structure.get("oracle_risk") == "low":
        score += 20
    return min(score, 100)


def analyze_amm(pool: dict) -> dict:
    """Analyze a constant-product AMM pool."""
    reserve0 = float(pool["reserve0"])
    reserve1 = float(pool["reserve1"])
    fee = float(pool.get("fee", 0.003))

    invariant = invariant_xyk(reserve0, reserve1)
    impact_small = price_impact(100, reserve0, reserve1)
    impact_large = price_impact(10000, reserve0, reserve1)

    return {
        "curve": "xyk",
        "invariant": invariant,
        "fee": fee,
        "invariant_stability": "high" if invariant > 1_000_000 else "medium",
        "price_impact_small": impact_small,
        "price_impact_large": impact_large,
        "volatility_exposure": "medium",
        "liquidity_depth": (
            "high" if (reserve0 + reserve1) > 1_000_000 else "medium"
        ),
        "oracle_risk": "medium",
    }


def lp_risk(position: dict) -> dict:
    """Estimate LP risk characteristics."""
    volatility = float(position.get("volatility", 0.5))
    impermanent_loss = volatility * 0.02
    fee_apr = float(position.get("fee_apr", 0.1))

    if volatility > 0.6:
        volatility_exposure = "high"
    elif volatility > 0.3:
        volatility_exposure = "medium"
    else:
        volatility_exposure = "low"

    return {
        "impermanent_loss_estimate": impermanent_loss,
        "fee_apr": fee_apr,
        "volatility_exposure": volatility_exposure,
    }


def analyze_yield(protocol: dict) -> dict:
    """Analyze a yield source."""
    real_yield = float(protocol.get("real_yield", 0.03))
    emissions = float(protocol.get("emissions", 0.02))
    synthetic = float(protocol.get("synthetic", 0.01))

    return {
        "real_yield": real_yield,
        "emissions": emissions,
        "synthetic_yield": synthetic,
        "yield_quality": "high" if real_yield > emissions else "medium",
    }


def analyze_lending(market: dict) -> dict:
    """Analyze lending-market utilization and liquidation risk."""
    supplied = float(market["supplied"])
    borrowed = float(market["borrowed"])
    collateral_factor = float(market.get("collateral_factor", 0.75))
    oracle_profile = market.get("oracle_profile", "standard")
    utilization = 0.0 if supplied <= 0 else borrowed / supplied

    if utilization > 0.8:
        liquidation_risk = "high"
    elif utilization > 0.5:
        liquidation_risk = "medium"
    else:
        liquidation_risk = "low"

    return {
        "utilization": utilization,
        "collateral_factor": collateral_factor,
        "liquidation_risk": liquidation_risk,
        "oracle_risk": {
            "redundant": "low",
            "standard": "medium",
            "fragile": "high",
        }.get(oracle_profile, "medium"),
    }


def analyze_bridge(bridge: dict) -> dict:
    """Analyze a bridge trust/finality profile."""
    finality = int(bridge.get("finality", 300))
    trust = bridge.get("trust", "optimistic")

    return {
        "finality_seconds": finality,
        "trust_model": trust,
        "oracle_risk": "high" if trust == "trusted" else "medium",
    }


def routing_graph(routes: list[str]) -> dict:
    """Summarize route count and MEV exposure."""
    route_count = len(routes)
    mev_exposure = "low" if route_count < 3 else "medium"
    return {
        "route_count": route_count,
        "mev_exposure": mev_exposure,
        "solver_network": "supported",
    }


def simulate_volatility(structure: dict) -> dict:
    return {
        "shock": "volatility",
        "impact": (
            "high" if structure.get("volatility_exposure") == "high" else "medium"
        ),
    }


def simulate_liquidity(structure: dict) -> dict:
    return {
        "shock": "liquidity_withdrawal",
        "impact": "high" if structure.get("liquidity_depth") == "low" else "medium",
    }


def simulate_oracle_failure(structure: dict) -> dict:
    return {
        "shock": "oracle_failure",
        "impact": "critical" if structure.get("oracle_risk") == "high" else "medium",
    }


def simulate_governance_change(structure: dict) -> dict:
    del structure
    return {"shock": "governance_change", "impact": "low"}


def simulate_fee_shift(structure: dict) -> dict:
    del structure
    return {"shock": "fee_shift", "impact": "medium"}


def run_defi_analysis() -> dict:
    """Run the default PCI DeFi analysis suite."""
    amm = analyze_amm({"reserve0": 500000, "reserve1": 800000, "fee": 0.003})
    lp = lp_risk({"reserve0": 500000, "reserve1": 800000, "volatility": 0.2})
    yield_analysis = analyze_yield(
        {"real_yield": 0.05, "emissions": 0.02, "synthetic": 0.01}
    )
    lending = analyze_lending(
        {"borrowed": 300000, "supplied": 800000, "oracle_profile": "redundant"}
    )
    bridge = analyze_bridge({"finality": 180, "trust": "optimistic"})
    routing = routing_graph(["eth->arb", "arb->base"])

    combined_structure = {
        "volatility_exposure": lp["volatility_exposure"],
        "liquidity_depth": amm["liquidity_depth"],
        "oracle_risk": lending["oracle_risk"],
    }

    scenarios = {
        "volatility": simulate_volatility(combined_structure),
        "liquidity": simulate_liquidity(combined_structure),
        "oracle_failure": simulate_oracle_failure(combined_structure),
        "governance_change": simulate_governance_change(combined_structure),
        "fee_shift": simulate_fee_shift(combined_structure),
    }

    resilience = score_resilience(
        {
            "invariant_stability": amm["invariant_stability"],
            "volatility_exposure": lp["volatility_exposure"],
            "liquidity_depth": amm["liquidity_depth"],
            "oracle_risk": lending["oracle_risk"],
        }
    )

    return {
        "amm": amm,
        "lp": lp,
        "yield": yield_analysis,
        "lending": lending,
        "bridge": bridge,
        "routing": routing,
        "scenarios": scenarios,
        "resilience_score": resilience,
    }
