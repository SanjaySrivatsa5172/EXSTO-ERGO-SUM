---
description: Run the pm-status workflow graph — parallel scouts sweep the project, a skeptic panel verifies high-severity findings, and one merge node writes the status report with ranked next actions.
argument-hint: optional focus area, e.g. "submission readiness" or "verification debt"
---

You are running the project-manager graph for this repository.

Call the Workflow tool with `{name: "pm-status"}` — the script lives at
`.claude/workflows/pm-status.js`. If the author gave a focus area, pass it
through: `{name: "pm-status", args: {focus: "$ARGUMENTS"}}`.

While the fleet runs, do not duplicate its work inline — the graph's scouts
cover repo state, version/count drift, verification debt, submission
readiness, and tooling health. Wait for the run to complete.

When the workflow returns:

1. Present its `report` markdown to the author unchanged (it is the
   deliverable), then add the run date yourself — the script cannot stamp
   dates (workflow scripts have no clock), so you date the report.
2. If `state` is `needs-attention`, restate the confirmed high-severity
   findings in one or two plain sentences above the report.
3. Do not act on any next action without the author's say-so — this graph is
   report-only, and so is this command.

If the Workflow tool is unavailable in this session (e.g. a restricted
harness), fall back to doing the five scout sweeps yourself inline, in the
same order, and say plainly that the run was inline rather than fleet.
