# contamination_scanner.py
import os, re, json, sys, pathlib

# --- config ---
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
MAX_BYTES = 2_000_000  # skip huge binaries
TEXT_EXTS = {".md",".txt",".rtf",".yml",".yaml",".json",".py",".ts",".js",".jsx",".tsx",".css",".html",".ini",".cfg",".toml",".csv"}
PROX_CHARS = 60

hard = [
 r"\bLuman\s+Sphere\b", r"\bCouncil\s+of\s+33\b", r"\b33(?:rd)?\s+Council\b", r"\bRed\s+Drift\b",
 r"\bSolkari\b", r"\bNyrex\b", r"\bDravari\b", r"\bPATRIOS\b", r"\bGodspark\b", r"\bVault\s*13\b",
 r"\bFlarewatch\b", r"\bBronze\s+Stillness\b", r"\bGranite\s+Condemnation\b", r"\bEcho\s+Market\b",
 r"\bVerdant\s+Maw\b", r"\bObsidian\s+Cradle\b", r"\bShattered\s+Basin\b"
]
soft = [
 r"\bCouncil\s+of\s+Thirty[- ]Three\b", r"\bthe\s+Thirty[- ]Three\b", r"\bLuman\b",
 r"\bVault\s+Thirteen\b", r"\bpale\s+vaults\b", r"\bnull\s+kin\b", r"\biron\s+veil\b",
 r"\bmeal\s+token(s)?\b", r"\bdrift\s+circles?\b"
]
style = [r"\bledger\b", r"\baccount\b", r"\bsum\b", r"\bhymn\b", r"\breliquary\b"]

# ambiguous terms needing proximity: high only if near another canon term
ambiguous_high = [r"\bApex\b", r"\bHelios\b", r"\bAesir\b", r"\bKemet\b", r"\bSphere\b"]

def is_textfile(p):
    if p.suffix.lower() in TEXT_EXTS: return True
    try:
        with open(p, "rb") as f:
            chunk = f.read(1024)
        return b"\0" not in chunk
    except Exception:
        return False

def find_all(patterns, text, flags=re.I):
    matches = []
    for pat in patterns:
        for m in re.finditer(pat, text, flags):
            matches.append({"term": pat, "start": m.start(), "end": m.end()})
    return matches

def severity_for(text, hits):
    # initial tally
    hard_hits = [h for h in hits if h["kind"]=="hard"]
    soft_hits = [h for h in hits if h["kind"]=="soft"]
    amb_hits  = [h for h in hits if h["kind"]=="amb"]
    style_hits= [h for h in hits if h["kind"]=="style"]

    sev = "LOW"
    if hard_hits:
        sev = "HIGH"
    elif soft_hits and (len(soft_hits) >= 2 or style_hits):
        sev = "MEDIUM"
    # escalate ambiguous to HIGH if within PROX_CHARS of any canonical (hard/soft)
    if amb_hits and (hard_hits or soft_hits):
        for a in amb_hits:
            for c in hard_hits + soft_hits:
                if abs(a["start"] - c["start"]) <= PROX_CHARS:
                    sev = "HIGH"
                    break
    return sev

def context(text, start, end, radius=80):
    s = max(0, start - radius)
    e = min(len(text), end + radius)
    return text[s:e].replace("\n", " ")

def scan_file(path):
    try:
        if not is_textfile(path): return None
        if path.stat().st_size > MAX_BYTES: return None
        text = path.read_text("utf-8", errors="ignore")
    except Exception:
        return None

    hits = []
    for m in find_all(hard, text):  m.update(kind="hard");  hits.append(m)
    for m in find_all(soft, text):  m.update(kind="soft");  hits.append(m)
    for m in find_all(style, text): m.update(kind="style"); hits.append(m)
    for m in find_all(ambiguous_high, text): m.update(kind="amb"); hits.append(m)

    if not hits: return None

    sev = severity_for(text, hits)
    samples = []
    for h in sorted(hits, key=lambda x: x["start"])[:8]:
        samples.append({
            "kind": h["kind"],
            "term": re.sub(r"\\b|\\s|\?|:|\(|\)|\+|\*|\[|\]|\\","", h["term"]),
            "snippet": context(text, h["start"], h["end"])
        })

    # collapse counts by kind
    counts = {"hard":0,"soft":0,"amb":0,"style":0}
    for h in hits: counts[h["kind"]] += 1

    return {
        "path": str(path),
        "severity": sev,
        "counts": counts,
        "samples": samples
    }

def main():
    root = pathlib.Path(ROOT)
    results = []
    for p in root.rglob("*"):
        if p.is_file():
            r = scan_file(p)
            if r: results.append(r)
    # sort: HIGH -> MEDIUM -> LOW
    order = {"HIGH":0,"MEDIUM":1,"LOW":2}
    results.sort(key=lambda x: (order.get(x["severity"],3), -x["counts"]["hard"], -x["counts"]["soft"]))
    out = {
        "scanned_root": str(root),
        "total_flagged_files": len(results),
        "files": results
    }
    pathlib.Path("contamination_report.json").write_text(json.dumps(out, indent=2), "utf-8")
    # human-readable summary
    lines = ["# Contamination Report",
             f"Root: {root}",
             f"Total flagged files: {len(results)}",
             ""]
    for r in results:
        lines.append(f"- **{r['severity']}** — {r['path']}  (hard:{r['counts']['hard']}, soft:{r['counts']['soft']}, amb:{r['counts']['amb']}, style:{r['counts']['style']})")
    pathlib.Path("contamination_report.md").write_text("\n".join(lines), "utf-8")
    print("Wrote contamination_report.json and contamination_report.md")

if __name__ == "__main__":
    main()
