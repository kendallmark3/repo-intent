# Candidate Open-Source Test Targets

Choose repositories you can legally clone and inspect. Favor diversity over fame.

## Recommended Test Shapes

### Target A — Small, obvious application
Purpose: establish baseline evidence precision and report usability.

Pick a repository with:
- a clear entry point;
- tests;
- a README;
- one datastore or external integration.

### Target B — Medium application with several layers
Purpose: test component boundaries and representative flow tracing.

Pick a repository with:
- API + service/domain + persistence;
- configuration;
- CI;
- tests;
- container/deployment artifacts.

### Target C — Framework/library/CLI
Purpose: ensure RepoIntent does not assume every repo is a web service.

### Target D — Repo you already know deeply
This is the most important test.

You should be able to challenge:
- system purpose;
- main entry points;
- important integrations;
- data flow;
- architecture claims;
- stale docs.

### Target E — Deceptive/stale repository
Useful signals:
- old README;
- unused dependencies;
- multiple entry points;
- examples mixed with production source;
- deprecated modules.

Purpose: test restraint.

## Selection Rule
Do not tune V1 to one repository family. Test different languages/frameworks so failures expose assumptions in the reasoning method rather than just parser gaps.
