# Plan: reconcile draft-03 with draft-ietf-sidrops-publication-server-bcp

**Status:** applied 2026-09-14. All 7 edits below are live in draft-sweetser-bcp-rpki-ca-02.md; rebuilt via mmark + xml2rfc --strict, citation resolves. (Originally built as -03; renumbered to -02 after the datatracker's submission API rejected -03 as a non-sequential revision — see README.md for the correction.)

## Why

`draft-ietf-sidrops-publication-server-bcp` (v10, 2026-08-27, awaiting AD go-ahead — the WG's own, further along than ours) sets MUST/SHOULD requirements for operating RFC 8181 publication engines and their RRDP/rsync repositories. Verified directly against its text (not just the survey's paraphrase):

- Publication engine **MUST** be highly available (§3.2); RRDP servers **MUST** be highly available (§5.4) — no specific percentage given.
- RRDP snapshot/delta files **SHOULD** remain available 2 hours after becoming unreferenced (§5.4).
- Publishers **SHOULD NOT** resync more than once per 10 minutes (§3.4); publication engines **RECOMMENDED** not to produce RRDP deltas more than once per minute (§5.5).
- Multi-backend load-balancing **MUST** provide a consistent view and update faster than RP refresh rate; new RRDP notification files **MUST NOT** precede their snapshot/delta (§5.9.1) — this is an atomicity requirement at the engine level.
- Monitoring availability/latency round-trip via re-issued-object tracking is **RECOMMENDED** (§3.2); close monitoring of performance metrics is **SHOULD** (§5.3).
- Explicitly does **not** cover CA lifecycle, dead/flapping CA detection, or revocation — confirming those sections of our draft are NOT in scope for this reconciliation.

Where our draft sets a number pub-server-bcp doesn't (99.5% availability, 10s response time, one-hour failover), that's our genuine contribution and stays. The actual problem is four spots where our text either restates a mechanism pub-server-bcp already owns, or uses a number close enough to one of theirs that a reader could mistake it for a conflict.

## Scope check — confirmed NOT overlapping, no changes proposed

Manifest Management (freshness/validity-period thresholds — CA content-generation decision, not engine ops), Data Integrity and Consistency (validation, audit logs, NTP — CA compliance, not engine ops), Operational Consistency (config management, staging), all of "Addressing Problematic CA Behaviors" (flapping/dead CA detection, revocation — pub-server-bcp explicitly excludes this), Registry Operator Monitoring/Responsibilities, CA Lifecycle Management, Implementation Considerations, Security Considerations.

## Proposed changes

### 1. Availability and Reliability Standards (lines 113–129)

Add one citation sentence to the section intro (line 115) noting pub-server-bcp already mandates high availability and redundancy for the publication engine itself; reframe this section as CA-operator-level policy targets built on that mandate, not a competing requirement.

> Delegated CA operators **MUST** implement robust infrastructure to ensure reliable service delivery. [@I-D.ietf-sidrops-publication-server-bcp] establishes that the publication engine itself **MUST** be highly available; the targets below give CA operators concrete, registry-adjustable numbers to plan against.

Cite `[@I-D.ietf-sidrops-publication-server-bcp]` §5.9.1 on the load-balancing/redundant-infrastructure bullet (line 120 or 126) rather than restating it independently.

### 2. Publication Practices (lines 142–147)

Two specific bullets:

- **Atomic publication** (line 144): add a citation — pub-server-bcp §5.9.1 already requires new RRDP notification files not precede their snapshot/delta, which is the engine-level mechanism for the same atomicity property. Reword to point there rather than re-derive it:
  > CA operators **MUST** implement atomic publication updates to prevent temporary inconsistencies between manifests and published objects, consistent with the RRDP publication ordering required by [@I-D.ietf-sidrops-publication-server-bcp].
- **30-minute update cap** (line 146): this is easy to misread as conflicting with pub-server-bcp's 10-minute resync cap (§3.4) and 1-minute delta-production recommendation (§5.5) — they're actually different things (CA's manifest-regeneration cadence vs. protocol-level resync/delta-production cadence), but a reviewer will ask. Add a clarifying clause:
  > CA operators **SHOULD NOT** publish manifest updates more frequently than every 30 minutes without operational justification. This governs how often a CA regenerates its manifest, distinct from the publication-engine resynchronization and RRDP delta-production limits in [@I-D.ietf-sidrops-publication-server-bcp].

### 3. Performance Issues (lines 214–231)

Add a citation to the section intro (line 216) making explicit that pub-server-bcp establishes availability/performance as a MUST in principle without specific numbers, and that this section supplies the numeric targets it deliberately leaves open:

> CA operators **MUST** ensure their infrastructure provides adequate performance for the global validator ecosystem. [@I-D.ietf-sidrops-publication-server-bcp] requires the publication engine to be highly available and monitored but does not set specific numeric targets; the following give registry operators a concrete baseline to adopt or adjust.

Cite pub-server-bcp §3.2's round-trip monitoring technique on the "MUST monitor response times and error rates continuously" bullet (line 227) as a recommended implementation method, rather than leaving it unsourced.

### 4. CA Operator Self-Monitoring — Required Monitoring Metrics (lines 239–246)

Cite `[@I-D.ietf-sidrops-publication-server-bcp]` §3.2/§5.3 on the "Publication point availability and response time" metric (line 241) — this is literally the monitoring technique that document recommends (tracking expected vs. observed re-issued-object appearance, watching for snapshot fallback).

## New backmatter reference needed

`I-D.ietf-sidrops-publication-server-bcp` is a live WG draft, not yet an RFC — mmark should resolve it automatically from the I-D bibxml index the same way it already does for other `[@I-D.xxx]`-style citations (already proven working for `I-D.ietf-sidrops-rpki-ccr` added this session). No manual `<reference>` block should be needed; verify after building.

## What this deliberately does NOT do

- Does not remove any numeric SLA target (99.5%, 10s response, one-hour failover, etc.) — pub-server-bcp doesn't set these, so they remain our draft's actual value-add.
- Does not touch CA lifecycle, flapping/dead-CA, or registry-enforcement content — confirmed out of scope for pub-server-bcp.
- Does not restructure section headers or merge sections — this is citation-and-clarification, not reorganization.

## Execution

Once approved: apply the ~6 edits above, rebuild with `mmark` + `xml2rfc --strict`, confirm the new citation resolves, run `idnits` again, and update the diff for review — same process as the rest of this renewal pass.
