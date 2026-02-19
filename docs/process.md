# Process (baseline)

**Cycle:** Weekly cadence (1-week cycles). Each cycle ends with a short sync and a small demo of completed work.

**Definition of Ready (DoR)** — an item is Ready if:
1. Goal and acceptance criteria are written in the issue.  
2. Tasks are small enough to finish within the cycle (prefer ≤ 2 dev-days).  
3. Owner assigned.

**Definition of Done (DoD)** — an item is Done when:
1. Code builds and automated checks/tests pass.  
2. Acceptance criteria met and documented in the PR.  
3. At least one peer approved the PR.  
4. Release notes / docs updated if behavior changed.

**PR & review flow**
- Create a feature branch named `feat/<short-desc>` or `fix/<short-desc>`.  
- Open a PR describing the change and link the issue.  
- Assign a reviewer (another team member). Reviewer verifies acceptance criteria, runs quick tests, and requests changes or approves.  
- Merge only after approval and passing checks.

**Evidence to keep**
- Keep issue ↔ PR link, reviewer comments, and CI/test results in the PR. These are the artifacts for checkpoint review.
