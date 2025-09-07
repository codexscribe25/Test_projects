# E1_S1 memory package
# README_MEMORY.md / README.md — preflight
preflight:
  description: "Documentation files; optional but recommended for operators."
  require_files:
    - "README_MEMORY.md"
    - "README.md"
  fail_on_missing: false

Contains:
- 05b_E1_S1-lore-approve-refs-20250904T133056Z.yml  -> ticket to validate + approve canon packets and append to MemoryLog_Lore.yml
- 00b_E1_S1-sync-theme-from-memory-refs-20250904T133056Z.yml -> ticket to regenerate Theme_LoreIndex.yml and Theme_Main.yml from MemoryLog_Lore.yml
- MemoryLog_Lore.yml (seeded) -> persistent project lore memory (single-writer via 05b ticket)

Usage:
1. After lore-audit produces canon_packet_stub.md, edit/fill the stub with required fields.
2. Run: `Run the ticket in 05b_E1_S1-lore-approve-refs-20250904T133056Z.yml`
   - Confirm validation and provide human ack when prompted.
   - This will append to MemoryLog_Lore.yml and emit logmarks.
3. To sync theme index/digests for other sessions, run:
   `Run the ticket in 00b_E1_S1-sync-theme-from-memory-refs-20250904T133056Z.yml`
4. Optionally re-run BOOT (00_E1_S1-BOOT.yml) if you rely on Theme_Lock.json regenerations.

Notes:
- Keep MemoryLog_Lore.yml as the authoritative canonical memory. Do not edit it directly; use 05b to append.
- logs/logmarks.ndjson is append-only and used for runtime events.
