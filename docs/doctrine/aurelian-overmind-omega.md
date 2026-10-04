# Aurelian Overmind Ω

**Source:** [`critter2881/aurelian-overmind-omega`](https://github.com/critter2881/aurelian-overmind-omega) (MIT).

## Purpose

A single-file Python program (`aurelian_overmind.py`, about 300 lines, standard library only) that generates a Whop storefront and a "Sovereign Total Value Index" from one source of truth.

## How it works

- **Truth engine:** rejects empty text and text containing banned non-real-world words.
- **Products:** dataclass records with a code, name, description, and perceived value.
- **CPVE / STVI:** counts products, divisions, engines, subsystems, and capabilities, then computes `index = (sum of counts) × perceived value × 15`, where 15 = 5 (sovereign) × 2 (ascension) × 1.5 (fractal).
- **Storefront:** renders markdown and a Whop payload from those numbers.

> **Important caveat.** Perceived value is a constant (`100` for every product, "10/10 or reject"). The index is therefore a **declared** figure derived from counts and fixed multipliers. It is a presentation device, not a measurement of real value. Present it accordingly in any customer-facing material.

## Decision

The code is self-contained and unrelated to this repository's runtime, so it was **not copied in**. It remains readable in its source repository. Recommended: archive the source repository, or tell me to import it into `tools/` with tests.
