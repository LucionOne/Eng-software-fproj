# Development Process

## Cycle
1-day development cycles. Each cycle must end with a working commit of at least one complete part.

## Definition of Ready (DoR)
A task is ready when:
1. All subtasks are clearly defined
2. Each subtask is small, focused, and achievable within the cycle
3. Basic implementation approach is documented

## Definition of Done (DoD)
A task is done when:
1. Code is complete and compiles/runs without errors
2. Integrates cleanly with existing components
3. Includes appropriate documentation and tests
4. A commit to main branch has been completed

## Branching & Review Flow
1. Create feature branch from `dev`
2. Implement parts incrementally
3. Request AI review before considering complete
4. Both implementation and review must agree part is ready
5. Keep complete parts in `dev` until feature is fully integrated
6. Merge feature to `main` only when fully tested

## Evidence Retention
- **Commit messages:** Reference feature/part ID and what was completed
- **Architecture history:** Document major design decisions in git log or this repo
- **Test results:** Include CI/CD output (when implemented)

## Part Definition
A "part" is:
- Smallest unit of work within a feature
- Ranges from single function to complete class
- Must be independently testable
- Must add clear value to the system