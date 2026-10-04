# Chapter 10 — Governance, Compliance, and Security

The [White Paper](../WHITEPAPER.md) is the governing document. This chapter turns it into working rules. It is operational guidance, **not legal advice**.

## Governance model

The white paper defines (sections): Scope and Objectives, Governance Model, Compliance Reference Framework, Documentation Standards, Repository Architecture Discipline, Automation and Build-Proof Standards, Risk Management and Control Areas, and Release and Maintenance Standards.

## Compliance references

- **U.S. Clarity Act** is referenced in the policy framework. Enterprise automation and compliance processes should stay aligned with it where applicable.
- **EU MiCA** is referenced as an international crypto-asset framework. Crypto-related products should be designed with attention to authorization, governance, disclosure, operational safeguards, and prudential considerations.
- Final compliance determinations belong to qualified legal and regulatory professionals.

## Security rules

| Rule | How it is enforced |
|------|--------------------|
| No secrets in source | Credentials come only from environment variables. `.env` is git-ignored. |
| Seeds and tokens never logged | Code reads `XRPL_WALLET_SEED` and `GITHUB_TOKEN` from the environment only. |
| Public data only in registries | Wallet registry holds addresses, never keys. |
| Errors don't leak internals | `500` returns a generic message; details go to logs. |
| Real-money actions are explicit | Minting defaults to testnet and mainnet needs `--mainnet`. |
| Dependencies from known sources | Declared in `requirements.txt`. |

If a secret is ever committed: **revoke it immediately**, then remove it from history. Deleting it in a later commit is not enough.

## Claims discipline

Marketing and doctrine statements (APO integrity percentages, "99.997%", reach-point counts) must be labeled as claims unless backed by evidence. Compliance outputs such as `/api/compliance/check` must be described as *format and pattern screens*, not regulatory clearance.

## Release checklist

Before a release, confirm: legal and policy alignment, security and access control, documentation completeness, no empty or obsolete artifacts, and a consistent structure across automation workflows (from the README's Review Expectations).

## Where to go next
[Chapter 11 — Development Workflow, Testing, and CI](11-development-workflow-and-ci.md)
