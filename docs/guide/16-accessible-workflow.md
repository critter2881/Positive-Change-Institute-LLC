# Chapter 16 — An Accessible, Low-Effort Workflow

This repository is set up so that the owner, can run and extend it with **as little typing and as little remembering as possible**. These are design requirements, and automated tests protect them.

## Principles

1. **One short word does one whole job.** No long commands to remember or type.
2. **The repository remembers, so you don't have to.** Status, next tasks, and history are one command away.
3. **Pick, don't type.** Forms use dropdowns; free text can be rough notes or dictated.
4. **Automation does the checking.** CI, security scans, and quant verification run without being asked.
5. **Nothing risky happens by accident.** Large or irreversible actions need explicit confirmation (Chapters 7 and 15).

## The short commands (`Makefile`)

Run `make` alone to list them.

| Type this | What it does |
|-----------|--------------|
| `make setup` | Installs everything (first time only) |
| `make check` | Lint and all tests, same as CI |
| `make verify` | Quant verification of the models |
| `make run` | Starts the API on port 5000 |
| `make apo` | Starts APO on port 8000 |
| `make status` | **"Where am I?"** Shows the branch, unsaved changes, last release, last verification result, and your next three open tasks |
| `make all` | `check`, `verify`, then `status` |

## No setup at all

`.devcontainer/devcontainer.json` makes **GitHub Codespaces** (or VS Code Dev Containers) build a ready environment in the browser with dependencies installed, ports forwarded, larger editor text, and **autosave**. Nothing needs to be installed on your own computer.

## Reducing typing

- **Voice:** use your operating system's dictation (Windows: `Win+H`; macOS: Fn twice; Android and iOS: the keyboard microphone) in GitHub's issue and comment boxes and in Codespaces.
- **Ask Copilot instead of typing code:** open an issue with the **Task** form (dropdowns plus one rough-notes box), and it is assigned automatically (Chapter 15). Describe the outcome in plain words.
- **Phone or tablet:** the GitHub mobile app can open issues, review, and merge pull requests without a keyboard-heavy workflow.
- **Large targets:** the web page's links and buttons are at least 44 px tall, so they are easier to hit.

## Reducing remembering

| Need | Where |
|------|-------|
| What is happening now? | `make status` |
| What changed, and when? | `CHANGELOG.md` |
| What is left to do? | `tasks.md` and the open issues |
| What does a word mean? | [Glossary](14-glossary.md) |
| How do I do X? | [Chapter 11](11-development-workflow-and-ci.md) recipes |
| Did the math checks pass? | The weekly **Quant verification** run, or `make status` |

## Accessibility of the public website

`frontend/index.html` meets this baseline, enforced by `tests/test_accessibility.py`: declared language, a "Skip to main content" link, a labeled main landmark and navigation, visible keyboard focus, reduced-motion support, alt text on images, and zoom not disabled. These are baseline checks, **not a full WCAG audit**. Colour contrast and screen-reader testing still need a manual pass.

## What "quant verified" covers

`make verify` checks that PCI's own models stay mathematically consistent (Chapter 15). It does not audit finances, markets, or legal compliance.

## Where to go next

