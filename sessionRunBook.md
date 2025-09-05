CLEAN_ROOM: true
memory_scope: project-only
import_user_knowledge_memories: false
allow_session_history_lookup: false

boot_sequence:
  - ticket_00_boot_gate.yml

Absolutely. Here’s a clean, **exact** step-by-step runbook that uses your existing tickets, adds *one* tiny Core-Deck boot/gate, and keeps isolation rock-solid.

---

# What to pin in the Core Deck (persistent; flat)

Use **2 slots**:

1. `projects_ledger.yml` – project identity & clean-room policy
2. `ticket_00_boot_gate.yml` – **extract ZIP → auto-detect overlay(s) → gate mount**

(You already have the ZIP tickets at session level; keep them in the repo ZIP.)

**Project Instructions (paste once, plain text):**

```
CLEAN_ROOM: true
memory_scope: project-only
import_user_knowledge_memories: false
allow_session_history_lookup: false

boot_sequence:
  - ticket_00_boot_gate.yml
```

---

# Session Runbook (new session + your repo ZIP)

**0) Upload your repo ZIP**

* Place it as: `/mnt/data/upload.zip`.

**1) Run `ticket_00_boot_gate.yml` (Core Deck)**

* Purpose: extract → detect `Theme/Overlays/*/` → gate everything else.
* Outputs (must exist after run):

  * `/mnt/data/build/overlay_paths.json` (array of allowed overlay paths)
  * `/mnt/data/build/context_pack.json` (audit of what’s mounted)

**2) Run `00_projects_preboot.yml` (from ZIP, optional but recommended)**

* Configure it to **read** `/mnt/data/build/overlay_paths.json` and **not add** any other overlay paths.
* Acceptance: its log shows only the detected overlay(s) are registered for this run.

**3) Run `00_map_virtual_cores.yml` (from ZIP)**

* Purpose: map your renamed COREs (`01_System_Policy.yml`, `02_ProjectCORE.yml`, `03_PromptPersonaCORE.yml`, `04_MemoryCORE.yml`, `05_NarrativeCORE.yml`, `06_VisionCORE.yml`, `07_OperatorsPlugins.yml`, `09_SpiralCORE.yml`) into whatever the downstream tickets expect (aliases/virtual mounts).
* Acceptance: a “core map” artifact (json/yml) listing these files with their virtual names.

**4) Run `00_E1_S1-BOOT.yml` (from ZIP)**

* Pass-through params (or environment) so it **consumes**:

  * `overlay_paths_from=/mnt/data/build/overlay_paths.json`
  * `context_pack=/mnt/data/build/context_pack.json`
  * Ensure it **does not** import any “user knowledge” outside this project (we already set that globally).
* Acceptance: BOOT log confirms active overlay(s) = exactly those in `overlay_paths.json`.

**5) Run `00a_E1_S1-session-snapshot.yml` (from ZIP)**

* Include references to:

  * `overlay_paths.json`
  * `context_pack.json`
  * the “core map” from step 3
* Acceptance: snapshot file written (list of mounted sources + checksums).

**6) Run `00b_E1_S1-sync-theme-from-memory-refs.yml` (from ZIP)**

* Important: run in **overlay-only** mode.

  * `import_user_knowledge_memories=false`
  * `refs_scope=overlay_only`
  * `overlay_paths_from=/mnt/data/build/overlay_paths.json`
* If this ticket can’t restrict scope, **skip it** (it’s the most common contamination vector).

**7) Run `00c_E1_S1-theme-validate.yml` (from ZIP)**

* Add a **report-only** provenance check (zero censorship). If you included a validator in the ZIP, wire it here (e.g. `validators/cross_theme_audit_min.yml` or your provenance guard).
* Acceptance: validation passes; if any WARN, you get a readable `provenance_note.md`.

**8) Run `00d_E1_S1-lore-deepscan.yml` (from ZIP)**

* Make sure it reads `context_pack.json` so scans stay within the mounted overlay.
* Acceptance: deepscan outputs (index/report) only reference the active overlay.

**9) (Optional) Run `00e_E1_S1-set-enforcement-phase.yml` → `00f_E1_S1-auto-evaluate-phase.yml`**

* Keep them **report-only** at first. Flip to enforcement later if desired.

---

## Quick acceptance checklist

* ✅ `/mnt/data/build/overlay_paths.json` exists and lists only your chosen overlay path(s).
* ✅ All tickets past step 1 reference `overlay_paths.json` / `context_pack.json`.
* ✅ No ticket reads outside the mounted overlay; any warnings are **reported**, not censored.
* ✅ Session snapshot and deepscan artifacts show only your active overlay.

---

## Notes on your uploaded tickets

You uploaded these (session-local) and they’re perfect to keep **in the ZIP**:

* `00_E1_S1-BOOT.yml`, `00a_E1_S1-session-snapshot.yml`, `00b_E1_S1-sync-theme-from-memory-refs.yml`, `00c_E1_S1-theme-validate.yml`, `00d_E1_S1-lore-deepscan.yml`, `00e_E1_S1-set-enforcement-phase.yml`, `00f_E1_S1-auto-evaluate-phase.yml`, `00_map_virtual_cores.yml`, `00_projects_preboot.yml`.

Just ensure **each** reads the gated list from `/mnt/data/build/overlay_paths.json` (and not from any global/default path).

---

If you want, I can generate a tiny **param shim** (`/mnt/data/build/run_params.json`) and one-line patches you can copy into each ticket so they automatically consume the gated paths without editing logic everywhere.
