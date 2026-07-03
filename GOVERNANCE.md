# Governance

## Purpose and authority

This document defines decision boundaries for Th3ory of Mind public projects.
Repository maintainers are accountable for scope, review, releases, and policy
enforcement. CODEOWNERS identifies required reviewers but does not grant access
or override repository permissions.

Final authority remains with authorized human maintainers. Automation and AI
tools may propose, analyze, test, or summarize changes; they may not approve,
merge, release, accept risk, or make governance decisions on behalf of a human.

## Decisions and review

Routine, reversible changes use pull-request review. Material architecture,
security-boundary, dependency, governance, or public contract decisions require
an architecture decision record (ADR) that records context, alternatives,
consequences, and the approving human.

A change to a public interface, schema, policy, event, manifest, or
compatibility contract also requires a migration plan. The plan must identify
affected consumers, compatibility strategy, validation, rollout, rollback, and
deprecation where applicable. These gates apply before merge, not after release.

## Provenance and signing

Contributors must identify generated and third-party material and comply with
applicable licenses. Tools may prepare commit or release metadata, but only an
authorized human may apply a cryptographic signature or attest that a change
was reviewed. A bot identity or generated signature must never be presented as
a human attestation.

## Amendments

Governance changes follow the same pull-request and CODEOWNERS review process.
Repository settings and applicable law take precedence if they conflict with
this document.

