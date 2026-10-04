# Decision — Human gating for Registry changes

**Date:** 2026-10-04  
**Research agent:** `research-synthesist`  
**Decision status:** proposed for implementation  
**Question:** How should changes to the Agent Registry and authority contracts be human-gated in a single-maintainer GitHub repository?

## Observed facts

1. GitHub CODEOWNERS can identify owners for repository paths and automatically request them for review on non-draft pull requests.
2. CODEOWNERS alone does **not** enforce approval. Required code-owner approval must be enabled through branch protection or a ruleset.
3. GitHub rulesets can require pull requests, status checks, review conditions and code-owner review on protected branches.
4. This repository is user-owned, not organization-owned. Team-based required reviewers are therefore not available here.
5. The current `agentic-factory` repository has no repository rulesets returned by the GitHub rulesets endpoint.
6. The connected GitHub integration cannot inspect branch-protection administration for this repository.
7. The repository currently has one human maintainer/owner in normal use. Requiring one approving review from another person would create a practical deadlock until a second collaborator with write access exists.

## Sources

Primary GitHub documentation:

- CODEOWNERS: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- Ruleset rules: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- Protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- Pull-request governance overview: https://docs.github.com/en/pull-requests/reference/managing-and-standardizing-pull-requests

Repository evidence:

- `GET /repos/eusouakell/agentic-factory/rulesets` returned an empty list on 2026-10-04.
- `.github/CODEOWNERS` did not exist before this decision.

## Interpretation

The Factory needs two distinct mechanisms:

### Ownership routing
Use `CODEOWNERS` now.

This documents which paths require human attention and scales correctly when additional collaborators are added.

### Enforcement
Use a `main` ruleset, but configure it in stages.

For a single-maintainer repository, enforcing a mandatory independent approval is not workable unless a second authorized reviewer exists. The enforceable baseline should therefore focus first on:

- pull requests before merge;
- required passing status checks;
- resolved review conversations;
- blocking force-push/deletion where appropriate.

Once a second reviewer with write access is available, add:

- at least one required approval;
- require review from Code Owners;
- dismiss stale approvals or require approval of the latest reviewable push.

## Decision

### Implement now in repository files

1. Add `.github/CODEOWNERS`.
2. Add a pull-request template that makes authority impact and human gates explicit.
3. Document change-control policy in `governance/change-control.md`.

### Manual repository-admin action

Create a ruleset targeting `main` with:

- **Require a pull request before merging**.
- **Require status checks before merging** → `Agent Registry Checks`.
- **Require conversation resolution before merging**.
- Do **not** require independent approval yet if Kell is the only reviewer with write access.

When a second human reviewer is added:

- require **1 approval**;
- enable **Require review from Code Owners**;
- enable stale-approval dismissal or latest-push approval.

## What this decision does not claim

- CODEOWNERS by itself is not a human gate.
- CI passing is not semantic approval.
- A ruleset cannot substitute for domain authority or publication approval.
- This research does not claim the current branch-protection state because the connected integration cannot read that admin endpoint.

## Confidence

**High** on GitHub feature behavior and the distinction between ownership routing and enforcement.  
**Medium** on the current admin configuration because branch-protection settings are not readable through the connected integration.

## Follow-up

Track the manual ruleset configuration as a repository issue. The Registry remains `pilot` regardless of this repository-level governance improvement.
