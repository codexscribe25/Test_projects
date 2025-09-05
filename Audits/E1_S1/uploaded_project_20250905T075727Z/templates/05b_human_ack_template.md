# 05b_human_ack_template.md — human approval block (YAML)
# Paste this block into canon_packet_stub.md (or save as 05b_human_ack.md) before running 05b approval ticket.
approver_name: "<Full Name>"
approver_role: "<Role / Title>"
approval_timestamp: "2025-09-04T00:00:00Z"   # ISO8601
approved: false        # set to true to approve and allow 05b to append to MemoryLog_Lore.yml
approval_method: "manual"   # e.g., manual | email | ticket-ui
canonical_id: "canon:<unique-id>"    # required if assigning canonical id at approval
term: "Short Term Name"              # human-friendly label for the lore entry
confidence_assessed: 0.75            # numeric 0.0 - 1.0
approval_notes: |
  - Brief rationale for approval or reasons to defer.
  - Any constraints, follow-ups, or editorial guidance.
changes_made: |
  - Describe edits applied to the draft/stub (line numbers or summary).
provenance_confirmed: false
provenance_notes: |
  - Evidence or citations used to confirm provenance (file paths, external refs).
sign_off_signature: "<initials or digital signature>"
related_ticket: "05_E1_S1-lore-audit-refs.yml"   # ticket that produced the stub (optional)
attachments:
  - filename: ""   # optional: list any attached artifacts used for approval
