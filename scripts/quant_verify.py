#!/usr/bin/env python3
"""
Quant verification: checks mathematical invariants of PCI's models.

The random seed rotates automatically (ISO year-week by default), so each
scheduled run exercises different inputs while staying reproducible: pass
``--seed N`` to replay a run.

Usage::

    python scripts/quant_verify.py [--seed N] [--samples N] [--output PATH]

Exit code is non-zero if any invariant fails.
"""

from __future__ import annotations

import argparse
import datetime
import json
import random
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from arcana_enterprise_nfts.arcana_nfts import arcana_nfts  # noqa: E402
from arcana_enterprise_nfts.evolution.engine import evolve  # noqa: E402
from backend.app import _compute_tokenomics  # noqa: E402
from backend.services.defi_analysis import (  # noqa: E402
    invariant_xyk,
    price_impact,
    run_defi_analysis,
)


def rotating_seed(today: datetime.date | None = None) -> int:
    """Return a seed that changes every ISO week."""
    iso = (today or datetime.date.today()).isocalendar()
    return iso[0] * 100 + iso[1]


def _check_tokenomics(rng: random.Random, failures: list) -> None:
    supply = rng.randint(1_000, 10**9)
    price = rng.uniform(0.0001, 100)
    dist = rng.uniform(0.01, 1.0)
    t = _compute_tokenomics(supply, price, dist)
    ctx = f"tokenomics(supply={supply}, price={price:.6f}, dist={dist:.4f})"
    if t["circulating_supply"] > supply:
        failures.append(f"{ctx}: circulating exceeds supply")
    if t["fully_diluted_valuation_usd"] + 0.01 < t["market_cap_usd"]:
        failures.append(f"{ctx}: FDV below market cap")
    pcts = [v["circulating_pct"] for v in t["vesting_schedule"]]
    if pcts != sorted(pcts) or pcts[-1] != 1.0 or any(p > 1.0 for p in pcts):
        failures.append(f"{ctx}: vesting not monotonic and ending at 1.0")


def _check_amm(rng: random.Random, failures: list) -> None:
    r0 = rng.uniform(1, 10**7)
    r1 = rng.uniform(1, 10**7)
    a1 = rng.uniform(0, r0)
    a2 = a1 + rng.uniform(0, r0)
    ctx = f"amm(r0={r0:.2f}, r1={r1:.2f})"
    if invariant_xyk(r0, r1) <= 0:
        failures.append(f"{ctx}: invariant not positive")
    i1, i2 = price_impact(a1, r0, r1), price_impact(a2, r0, r1)
    if not (0 <= i1 <= i2 < 1):
        failures.append(f"{ctx}: price impact not monotonic within [0, 1)")


def _check_resilience(failures: list) -> None:
    score = run_defi_analysis()["resilience_score"]
    if not 0 <= score <= 100:
        failures.append(f"resilience score out of range: {score}")


def _check_evolution(rng: random.Random, failures: list) -> None:
    for nft in arcana_nfts:
        low = rng.uniform(0, 600)
        high = low + rng.uniform(0, 600)
        a, b = evolve(nft, low), evolve(nft, high)
        if a["evolving"] and (b["level"] < a["level"] or len(b["traits"]) < len(a["traits"])):
            failures.append(f"{nft['product_id']}: evolution regressed as score increased")


def verify(seed: int, samples: int) -> dict:
    rng = random.Random(seed)
    failures: list = []
    for _ in range(samples):
        _check_tokenomics(rng, failures)
        _check_amm(rng, failures)
        _check_evolution(rng, failures)
    _check_resilience(failures)
    return {
        "verified": not failures,
        "seed": seed,
        "samples": samples,
        "failures": failures[:50],
        "failure_count": len(failures),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--samples", type=int, default=500)
    parser.add_argument("--output", default=str(_ROOT / "reports" / "quant_verification.json"))
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else rotating_seed()
    result = verify(seed, args.samples)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
