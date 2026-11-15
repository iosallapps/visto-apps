#!/usr/bin/env python3
"""Render legal sections into a site whose i18n swaps innerHTML from
data-en / data-ro attributes (TopoXY style). Replaces everything between
<!--legal:start--> and <!--legal:end--> (or, the first time, the given
start/end line markers) in privacy.html and terms.html.

    python3 adapters/data_attr.py apps/topoxy.json ~/Developer/topoxyapp-website
"""
import html, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import legal

TITLES = {"privacy": ("Privacy Policy", "Politica de confidențialitate"),
          "terms": ("Terms of Use", "Termeni de utilizare")}


def attr(s):
    return html.escape(s, quote=True)


def render(kind, sections, facts):
    en_t, ro_t = TITLES[kind]
    up_en = legal.fmt_date(facts["updated"], "en"); up_ro = legal.fmt_date(facts["updated"], "ro")
    out = ["<!--legal:start-->",
           f'<h1 data-en="{attr(en_t)}" data-ro="{attr(ro_t)}">{en_t}</h1>',
           f'<p class="last-updated" data-en="{attr("Last updated: " + up_en)}" data-ro="{attr("Ultima actualizare: " + up_ro)}">Last updated: {up_en}</p>',
           '<nav class="legal-toc" aria-label="Contents"><ol>']
    for i, s in enumerate(sections, 1):
        out.append(f'<li><a href="#{s["id"]}" data-en="{attr(s["en"]["h"])}" data-ro="{attr(s["ro"]["h"])}">{s["en"]["h"]}</a></li>')
    out.append("</ol></nav>")
    for i, s in enumerate(sections, 1):
        out.append(f'<section id="{s["id"]}" class="legal-section">')
        out.append(f'<h2 data-en="{attr(f"{i}. " + s["en"]["h"])}" data-ro="{attr(f"{i}. " + s["ro"]["h"])}">{i}. {s["en"]["h"]}</h2>')
        out.append(f'<div data-en="{attr(s["en"]["html"])}" data-ro="{attr(s["ro"]["html"])}">{s["en"]["html"]}</div>')
        out.append("</section>")
    out.append("<!--legal:end-->")
    return "\n".join(out)


def main():
    facts = json.loads(Path(sys.argv[1]).read_text()) if Path(sys.argv[1]).is_absolute() else json.loads((Path(__file__).resolve().parent.parent / sys.argv[1]).read_text())
    site = Path(sys.argv[2]).expanduser()
    built = legal.build(facts)
    for kind in ("privacy", "terms"):
        page = site / f"{kind}.html"
        t = page.read_text()
        block = render(kind, built[kind], facts)
        if "<!--legal:start-->" in t:
            t = re.sub(r"(?s)<!--legal:start-->.*?<!--legal:end-->", lambda m: block, t)
        else:
            t = re.sub(r'(?s)(<div class="legal-page">).*?(</div>\s*</main>)', lambda m: m.group(1) + "\n" + block + "\n" + m.group(2), t, count=1)
        page.write_text(t)
        print("wrote", page)

if __name__ == "__main__":
    main()
