

# Backlog v0.1 — Calculator Project

## Overview

Minimal, testable feature set for a calculator-themed portfolio submission. Implement in a single repo with unit tests and simple UI (CLI or minimal GUI).

## Functional Requirements (FR)

* **FR1 — Basic arithmetic (Must Have)**: support addition, subtraction, multiplication, division with integer and decimal operands.
* **FR2 — Input handling (Must Have)**: accept keyboard input, handle clear/backspace, and show error on invalid input (e.g., division by zero).
* **FR3 — Result display (Must Have)**: display results with up to 12 significant digits.
* **FR4 — Operator precedence & parentheses (Should Have)**: evaluate expressions respecting precedence and parentheses.
* **FR5 — Memory functions (Could Have)**: memory store (M+), recall (MR), clear memory (MC).
* **FR6 — Scientific functions (Won't Have v0.1)**: sin, cos, log — deferred to later releases.

> Classification uses MoSCoW (Must/Should/Could/Won't).

## Non-Functional Requirements (NFR)

* **NFR1 — Response latency**: UI must show result within **50 ms** after user presses Enter on a typical student laptop (reason: interactive feel and grading expectation). *Measurable by automated timing tests.*
* **NFR2 — Accuracy**: numeric results must match IEEE-754 double precision for floating operations, and integer ops must be exact for 64-bit signed integers. *Measurable by unit tests covering edge cases.*
* **NFR3 — Memory footprint**: application memory usage must remain **< 100 MB** when idle (reason: supports older lab machines). *Measurable by platform memory tools.*

*Justification*: NFRs are chosen because they are testable and relevant to where student code usually runs (personal/lab laptops) — avoid vague terms like "fast" or "secure" without metrics.

## Constraints

* **Language / Platform**: Implement in **C# (.NET 7)** and run on Windows 10/11 (student environment). If you prefer cross-platform, target .NET SDK that runs on Linux too.
* **No external paid libraries**: use only free/open-source packages or standard library.
* **No network access required**: app must run fully offline.
* **Repo structure**: files must live under `docs/requirements/` and be added via commits/PRs.

## Definition of Done (DoD) — example for a Must Have

**Target item**: FR1 — Basic arithmetic
**Acceptance criteria** (all must be true):

1. Automated unit tests (≥ 20 cases) validate addition, subtraction, multiplication, division for positive/negative integers, decimals, and edge cases (large numbers). All tests pass in CI.
2. Manual test: enter `3.5 + (-2) * 4` ⇒ display `-4.5` (operator precedence respected if FR4 implemented; if not, explicit tests for sequential operations must pass).
3. Division by zero returns a visible error message (no crash) and corresponding unit test asserts the error path.
4. Build succeeds on the specified .NET SDK and a PR merges into main with the new files present under `docs/requirements/`.
5. Measured average latency for the tested cases is < 50 ms.

## Minimal Evidence (what to deliver)

* Commits / PRs adding:

  * `docs/requirements/stakeholders.md`
  * `docs/requirements/backlog.md`
* A short unit test file (e.g., `Calculator.Tests`) demonstrating the automated tests for FR1.
* A README snippet noting the platform and how to run tests (`dotnet test`).

## Notes / Rules

* **Testability**: If you cannot measure or test something, mark it as a *wish* (not an NFR).
* **Prioritization**: pick a small, clear "Must Have" set — here FR1–FR3. Everything else is lower priority.
* **Justify NFRs**: each NFR above includes a reason tied to constraints or expected deployment.

---
