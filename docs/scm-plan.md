# Source Code Management Plan

## 1.1 Política de Branching

**Model adopted:** GitHub Flow variant (feature branches from `dev`, main for stable releases)

**Rationale:**
- Single `main` branch as the stable reference reduces complexity compared to GitFlow (which requires multiple long-lived branches).
- `dev` branch serves as the integration branch where features are tested together before merging to `main`, allowing team members to work in parallel on feature branches without blocking the main release line.
- This approach matches the existing repository structure (currently HEAD is on `dev`) and the DoD in docs/other/Process.md, which specifies "Merge feature to `main` only when fully tested."

**Branch naming conventions:**

- `feat/<scope>` — New feature (e.g., `feat/dashboard-ui`, `feat/sensor-contract-tests`)
- `fix/<scope>` — Bug fix (e.g., `fix/api-routing-duplicate`)
- `docs/<scope>` — Documentation changes (e.g., `docs/test-strategy`)
- `refactor/<scope>` — Code refactoring without behavior change (e.g., `refactor/datapuller-async`)
- `chore/<scope>` — Build, tooling, or maintenance (e.g., `chore/add-pytest-config`)

**Merge authority:**

- Any team member may create and push feature branches.
- Merges to `dev` are allowed after at least one peer review (or self-review + passing tests for urgent fixes).
- Merges to `main` require explicit approval and are restricted to project leads (Guilherme P. Santos) to ensure stability.
- Commits referenced in DoD (docs/other/Process.md) should be made to the appropriate branch with clear feature/part references.

## 1.2 Proteção da branch main

**Rules applied to `main` branch:**

- **Pull Request required:** no direct push; all changes must be submitted via a PR on GitHub.
- **Minimum approvals:** 1 approval required from repository maintainers before merge (Guilherme P. Santos or designated reviewer).
- **Justification for 1 approval:** Small, focused team; rapid iteration cycles (1-day sprints per docs/other/Process.md); approval serves as gate to catch obvious regressions before release. Will be escalated to 2+ for larger team or after v1.0 stability is reached.
- **Status checks required:**
  - **[TODO: configure CI pipeline]** Unit tests must pass (`python -m pytest tests/ -v` from docs/NEXT_STEPS.md).
  - **[TODO: configure CI pipeline]** Linting should pass (no specific linter configured yet; recommend `pylint` or `flake8` for Python).
- **Additional rules:**
  - **No force push** to `main`; maintains linear, auditable history.
  - **Branch protection:** delete head branch after merge to keep repository clean.
  - **Commit history:** maintain readable commit log for forensics and auditing (see convention below).

## 1.3 Convenção de Commits

**Standard adopted:** Conventional Commits (subset)

**Specification:** https://www.conventionalcommits.org/

**Format:**
```
<type>(<scope>): <subject>

<body (optional)>

<trailer (optional)>
```

**Examples from this project:**

1. **feat(datapuller): add ISO 8601 datetime validation**
   ```
   feat(datapuller): add ISO 8601 datetime validation
   
   DataPuller._translate_from_api now rejects invalid datetime formats
   and logs them instead of persisting corrupted data. Addresses validation
   boundary strategy in docs/Strategy.md.
   
   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
   ```

2. **fix(apiservice): remove duplicate /data endpoint**
   ```
   fix(apiservice): remove duplicate /data endpoint
   
   APIService.py had two @app.get("/data") handlers. Consolidated into
   single handler with optional after_id parameter per RFC requirements.
   
   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
   ```

3. **docs(test-strategy): add contract test ADR and scoping**
   ```
   docs(test-strategy): add contract test ADR and scoping
   
   Created docs/test-strategy.md with risk matrix, test level definitions,
   contract testing ADR, and regression strategy per A1-6 directive.
   Evidence placeholders indicate missing provider contract tests for v0.2.
   
   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
   ```

---
