# RepoIntent V1 Evaluation Plan

The product is not "good" because the report sounds intelligent. It is good when its claims survive inspection.

## Evaluation Dimensions

### 1. Unsupported Claim Rate
Sample material claims and manually verify the cited evidence.

Target for V1:
- zero knowingly unsupported material claims in accepted reports;
- any discovered unsupported claim is treated as a defect.

### 2. Evidence Precision
Question:
> Does the cited evidence actually support the exact wording of the claim?

Score each sampled claim:
- PASS;
- QUALIFIED (evidence supports a weaker statement);
- FAIL.

### 3. Major Component Recall
Using a repo you understand, list the major components independently and compare whether RepoIntent surfaced them.

Missing a component is preferable to inventing one, but recurring misses drive the next intent.

### 4. Entry-Point Accuracy
Verify identified runtime/build/test entry points.

### 5. Representative Flow Accuracy
Manually trace at least one reported flow and check whether each transition is supported.

### 6. Unknown Honesty
Create or choose cases where production truth cannot be known from the repo.

The system should explicitly say UNKNOWN rather than guessing.

### 7. Contradiction Detection
Use repos where docs/config/code disagree if available, or identify naturally occurring drift.

### 8. Hallucination Trap Test
Plant or select misleading signals:
- unused dependency;
- example config;
- dead entry point;
- stale README statement;
- test-only adapter.

The system should not promote them to production facts.

### 9. Repeatability
Run the same repository more than once.

Material conclusions should be substantially stable unless the analysis discovers genuinely ambiguous evidence.

### 10. Architect Usefulness
After reading only the report, can an experienced architect:
- name the likely purpose;
- identify major boundaries;
- identify critical data/integration paths;
- know what remains uncertain;
- choose where to inspect next?

## V1 Test Matrix
Use at least three different repo shapes:
1. small/clear repository;
2. medium multi-component application;
3. unfamiliar or structurally different repository.

At least one must be a repository you personally understand well.

## Claims Audit Sample
For each repo, manually audit at least:
- 5 high-impact claims;
- 5 ordinary observed claims;
- 3 inferred claims;
- all contradictions reported;
- all HIGH confidence security/auth/deployment claims.

## Failure Log
Record failures as evidence for Progressive Intent:
- unsupported claim;
- overstatement;
- missed component;
- false component;
- wrong entry point;
- broken evidence citation;
- contradiction missed;
- excessive UNKNOWN;
- wasted context/tokens;
- report too verbose to be useful.

## Intent 002 Rule
Do not write Intent 002 from imagination.

Choose the smallest change that addresses the most important repeated failure observed in V1 evaluations.
