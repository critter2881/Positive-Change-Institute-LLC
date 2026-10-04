#!/usr/bin/env python3
"""
APO measurement harness.

Measures what can honestly be measured about APO *in this repository* and
lists the claims that cannot be measured here.

Measured (local, loopback only):
  * Integrity: every API response is valid JSON and byte-identical to its
    reference digest across N requests; a deliberate one-byte corruption must
    be detected (the check has to be able to fail).
  * Latency: p50 / p95 / p99 / max over loopback HTTP, compared with the
    claimed 0.08 s. This is local latency, not "global" delivery.

Not measurable here (no validator network, satellites or legacy baseline):
  14,000+ reach points, 7-orbit redundancy, +480% reliability, 12-layer
  enforcement outcomes, quantum resilience.

Usage::

    python scripts/apo_measure.py [--requests N] [--output PATH]

Exit code is non-zero if any integrity check fails or latency exceeds the
claim. The report includes a one-sided Wilson upper bound (95%); a clean run
does not prove 99.997% unless N is at least 100,000.
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import statistics
import sys
import threading
import time
from http.server import ThreadingHTTPServer
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from apo import apo  # noqa: E402

ENDPOINTS = ["/api/apo_stats", "/api/meta", "/api/apo_whitepapers", "/api/apo_docs"]
CLAIMED_INTEGRITY = 0.99997
CLAIMED_LATENCY_S = 0.08
_WILSON_Z_95 = 1.6448536269514722
UNMEASURABLE = [
    "14,000+ validator reach points",
    "7-orbit satellite redundancy",
    "+480% cross-chain reliability (no legacy baseline)",
    "12-layer doctrine enforcement outcomes",
    "quantum-resilient security",
    "global delivery time (only loopback latency is measured)",
]


def digest(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def corruption_detected(reference: dict) -> bool:
    """A one-byte change to a payload must change its digest."""
    path = ENDPOINTS[0]
    body = bytearray(apo.Router.route(None, path)[1].encode())
    body[0] ^= 0x01
    return digest(bytes(body)) != reference[path]


def percentile(values: list[float], pct: float) -> float:
    ordered = sorted(values)
    idx = min(len(ordered) - 1, int(round(pct / 100 * (len(ordered) - 1))))
    return ordered[idx]


def failure_rate_upper_bound(failures: int, requests: int) -> float:
    """Return the one-sided 95% Wilson upper bound for a binomial rate."""
    rate = failures / requests
    z2 = _WILSON_Z_95**2
    denominator = 1 + z2 / requests
    center = rate + z2 / (2 * requests)
    margin = _WILSON_Z_95 * (
        rate * (1 - rate) / requests + z2 / (4 * requests**2)
    ) ** 0.5
    return (center + margin) / denominator


def measure(requests: int) -> dict:
    reference = {
        p: digest(apo.Router.route(None, p)[1].encode()) for p in ENDPOINTS
    }
    server = ThreadingHTTPServer(("127.0.0.1", 0), apo.Router)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    latencies: list[float] = []
    failures = 0
    try:
        for i in range(requests):
            path = ENDPOINTS[i % len(ENDPOINTS)]
            start = time.perf_counter()
            conn.request("GET", path)
            resp = conn.getresponse()
            body = resp.read()
            latencies.append(time.perf_counter() - start)
            ok = resp.status == 200 and digest(body) == reference[path]
            if ok:
                try:
                    json.loads(body)
                except ValueError:
                    ok = False
            failures += 0 if ok else 1
    finally:
        conn.close()
        server.shutdown()
        server.server_close()

    rate = 1 - failures / requests
    upper = failure_rate_upper_bound(failures, requests)
    return {
        "requests": requests,
        "failures": failures,
        "integrity_rate": rate,
        "failure_rate_upper_bound_95": upper,
        "supports_claimed_integrity": failures == 0
        and round(upper, 9) <= round(1 - CLAIMED_INTEGRITY, 9),
        "corruption_detected": corruption_detected(reference),
        "latency_s": {
            "p50": percentile(latencies, 50),
            "p95": percentile(latencies, 95),
            "p99": percentile(latencies, 99),
            "max": max(latencies),
            "mean": statistics.fmean(latencies),
        },
        "claimed_latency_s": CLAIMED_LATENCY_S,
        "claimed_integrity": CLAIMED_INTEGRITY,
        "not_measurable_here": UNMEASURABLE,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--requests", type=int, default=2000)
    parser.add_argument("--output", default="reports/apo_measurement.json")
    args = parser.parse_args()
    if args.requests < 1:
        parser.error("--requests must be at least 1")

    result = measure(args.requests)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))

    lat = result["latency_s"]
    print(f"requests={result['requests']} failures={result['failures']}")
    print(f"failure-rate upper bound (95%): {result['failure_rate_upper_bound_95']:.2e}")
    print(
        "supports 99.997% claim: "
        f"{result['supports_claimed_integrity']} (needs >= 100,000 requests)"
    )
    print(f"corruption detected: {result['corruption_detected']}")
    print(f"latency p50={lat['p50']*1000:.2f}ms p99={lat['p99']*1000:.2f}ms")
    print("Not measurable here: " + "; ".join(UNMEASURABLE))
    ok = (
        result["failures"] == 0
        and result["corruption_detected"]
        and lat["p99"] <= CLAIMED_LATENCY_S
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
