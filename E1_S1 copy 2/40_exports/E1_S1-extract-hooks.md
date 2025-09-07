Done — I ran the `E1_S1-extract-hooks-inline.yml` ticket and extracted inline narrative hooks from the exported episode. Outputs saved to the workspace; summary below.

Files produced

* Hooks YAML (structured): sandbox:/mnt/data/50\_extracted\_hooks/E1\_S1\_hooks.yml
* Annotated episode (inline hook markers): sandbox:/mnt/data/50\_extracted\_hooks/episode1\_final\_annotated.md
* Process log: sandbox:/mnt/data/logs/ExtractHooks\_Log.csv

What I extracted (high level)

* Characters (detected by capitalization heuristic + counts; role guesses): Rian (primary), Lette (supporting), Registrar (institutional), and other capitalized names found in the text. Full list is in the YAML.
* Objects: ledger, binding, kettle, chair, market, shop, basket, twine, paper, child, coat, pot, crate, seal, stoop, window.
* Places: market, alley, office, registrar, dock, bakery, staircase, table, window, neighborhood.
* Themes: debt, memory, favor, secrecy, choice, cost, kindness, power, safety, trust, record, registration, truth, justice, community, corruption, watch.
* Threads / plot hooks:

  * `blank_line` — interrupted ledger entry / blank line needing closure (HIGH).
  * `men_badges` — two men with badges who question Rian (HIGH; institutional interest / threat).
  * `neighbor_filled_line` — a neighbor later fills a line in ledger (MED).
  * `registrar_watch` — registrar expected to file and stamp (MED).
  * `next_name` — Rian intends to call the next person on the list (HIGH).

What the annotated export contains

* Inline markers inserted at the first mention of the major hooks, for example:

  * `Rian [HOOK:character:Rian:primary]`
  * `Lette [HOOK:character:Lette:supporting]`
  * `ledger [HOOK:object:ledger]`
  * the blank-line sentence annotated with `[HOOK:thread:blank_line]`
* The annotated file begins with a header noting the hooks YAML and timestamp.

Where to look for the details

* Open the hooks YAML to see the full structured extraction (characters with counts, objects, places, themes, threads, and scene hook snippets).

  * sandbox:/mnt/data/50\_extracted\_hooks/E1\_S1\_hooks.yml
* Open the annotated copy to see inline markers within the episode text.

  * sandbox:/mnt/data/50\_extracted\_hooks/episode1\_final\_annotated.md

Suggested next actions (pick any)

1. Run `hook_promote` to convert high-importance threads into concrete prompt\_jobs (e.g., "investigate\_badges", "follow\_blank\_line") with suggested beat scenes. I can generate those now.
2. Run a `continuity_scan` to cross-check extracted hooks against Theme\_LoreIndex.yml once you populate the index (will enable canon-linking).
3. Run a `character-sheet` generator for extracted characters (Rian, Lette) to produce quick stat blocks and motives for use in future episodes.
4. If you want fewer/more markers, I can re-run extraction with different heuristics: strict NER, lower-case keyword matching, or include dialogues only.

If you want, I can now:

* produce the `hook_promote` ticket outputs (prompt\_jobs) for the top 3 hooks, or
* attach the hook YAML and annotated file into a zip and provide a download link.

Which would you like next?
