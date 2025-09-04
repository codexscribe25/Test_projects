# canon_packet_stub.md — preflight
preflight:
  description: "Human-fillable stub produced by lore-audit; must contain required fields before approval."
  require_fields:
    - "canonical_id"
    - "term"
    - "short_description"
    - "created_by"
    - "approval block (approver_name, approval_timestamp, approved:true)"  # for 05b
  require_files:
    - "canon_packet_stub.md"
  fail_on_missing: true
---
canonical_id: "canon:placeholder-000"     # assign unique canonical id (canon:<slug>)
term: "Short Term Name"                  # human-friendly name
short_description: "One-line summary (1-2 sentences)." 
first_appearance:
  file: "10_drafts/episode1_v1.md"
  line_hint: 120
confidence: 0.65                          # 0.0 - 1.0 (author's initial assessment)
status: "proposed"                        # draft | proposed | approved | deprecated
created_by: "your-name"
created_ts: "2025-09-04T13:40:00Z"
provenance:
  - note: "Origin / evidence / citation"
    ticket: "05_E1_S1-lore-audit-refs.yml"
    artifact: "10_drafts/episode1_v1.md"
references:
  - artifact_path: "40_exports/episode1_final.md"
    anchor: "para-12"
tags:
  - tag1
  - tag2
notes: |
  Add any clarifying notes, constraints, or editorial cautions here.
---

# Canon Packet — Instructions
Fill all frontmatter fields above. Ensure `short_description`, `provenance`, and `created_by` are complete. If the item is not yet ready for approval, keep `status: proposed`.

---

# Suggested body (optional)
Use this space to expand the canonical entry for editorial review. Include examples, quotes, or cross-references.

---

# APPROVAL BLOCK (REQUIRED for 05b)
Paste this block at the end of the file or save as a separate `05b_human_ack.md` to be provided to the approval ticket. The approval ticket **will not** append to MemoryLog unless `approved: true` and approver metadata are present.

```yaml
approver_name: "<approver full name>"
approver_role: "<approver role/title>"
approval_timestamp: "2025-09-04T14:00:00Z"
approved: false        # set to true to approve and allow 05b to append
confidence_assessed: 0.90
approval_notes: |
  - Reason for approval or items to follow up on.
changes_made: |
  - List of edits applied by approver (line numbers or descriptions).
provenance_confirmed: true
provenance_notes: |
  - Any extra provenance details to record.
sign_off_signature: "<initials or digital signature>"
