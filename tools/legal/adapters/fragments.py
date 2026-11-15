#!/usr/bin/env python3
"""Write the legal sections as plain HTML fragments, one file per page and language:
<out>/privacy.en.html, privacy.ro.html, terms.en.html, terms.ro.html (+ sections.json).
Use when a site's i18n is not data-en/data-ro (path-based /ro/ pages, Next.js...):
the site's own code or a small script pastes the fragments in.

    python3 adapters/fragments.py apps/<slug>.json <out_dir>
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import legal

TITLES = {"privacy": {"en": "Privacy Policy", "ro": "Politica de confidențialitate"},
          "terms": {"en": "Terms of Use", "ro": "Termeni de utilizare"}}
UPD = {"en": "Last updated", "ro": "Ultima actualizare"}

def main():
    fp = Path(sys.argv[1]); fp = fp if fp.is_absolute() else Path(__file__).resolve().parent.parent / fp
    facts = json.loads(fp.read_text()); out = Path(sys.argv[2]).expanduser(); out.mkdir(parents=True, exist_ok=True)
    built = legal.build(facts)
    (out / "sections.json").write_text(json.dumps(built, ensure_ascii=False, indent=1))
    for kind, secs in built.items():
        for lang in ("en", "ro"):
            h = [f'<h1>{TITLES[kind][lang]}</h1>',
                 f'<p class="last-updated">{UPD[lang]}: {legal.fmt_date(facts["updated"], lang)}</p>',
                 '<nav class="legal-toc" aria-label="Contents"><ol>']
            h += [f'<li><a href="#{s["id"]}">{s[lang]["h"]}</a></li>' for s in secs]
            h.append("</ol></nav>")
            for i, s in enumerate(secs, 1):
                h.append(f'<section id="{s["id"]}" class="legal-section"><h2>{i}. {s[lang]["h"]}</h2>{s[lang]["html"]}</section>')
            (out / f"{kind}.{lang}.html").write_text("<!--legal:start-->\n" + "\n".join(h) + "\n<!--legal:end-->\n")
            print("wrote", out / f"{kind}.{lang}.html")

if __name__ == "__main__":
    main()
