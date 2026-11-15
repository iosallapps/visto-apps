#!/usr/bin/env python3
"""Build step for vistoapps.com. Run after editing any page or js/data.js:

    python3 tools/build.py

The English pages at the repo root are the source. This script:
  - writes the SEO head (canonical, hreflang, Open Graph, Twitter, JSON-LD) into every page,
  - fills the generated blocks (app legal links),
  - generates the Romanian pages under /ro/ from the strings in js/data.js,
  - writes sitemap.xml with both languages.
It is idempotent: running it twice gives the same files.
"""
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://vistoapps.com"
PAGES = ["index.html", "apps.html", "about.html", "contact.html", "privacy.html", "terms.html", "404.html"]
INDEXABLE = [p for p in PAGES if p != "404.html"]
OG_IMAGE = SITE + "/assets/logo/og-image.png"
LOCALES = {"en": "en_US", "ro": "ro_RO"}
# schema.org applicationCategory per App Store genre
SCHEMA_CATEGORY = {
    "kupfra": "UtilitiesApplication", "pdfino": "UtilitiesApplication", "darc": "UtilitiesApplication",
    "agrondo": "BusinessApplication", "luris": "HealthApplication", "appsrank": "DeveloperApplication",
    "topoxy": "TravelApplication", "kipply": "UtilitiesApplication", "serenity": "HealthApplication",
    "shelfready": "MultimediaApplication",
}

GEN_SEO = re.compile(r"\s*<!--gen:seo-->.*?<!--/gen:seo-->", re.S)
OLD_SEO = re.compile(r'\s*<(?:link rel="canonical"|link rel="alternate"|meta property="og:[^"]*"|meta name="twitter:[^"]*"|meta name="robots")[^>]*>')


def load_data():
    js = "global.window={};require(%s);console.log(JSON.stringify({V:window.VISTO,RO:window.VISTO_RO}))" % json.dumps(str(ROOT / "js/data.js"))
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    return d["V"], d["RO"]


def page_name(file):
    return "home" if file == "index.html" else file[:-5]


def url_for(lang, file):
    path = "" if file == "index.html" else file
    return SITE + ("/ro/" if lang == "ro" else "/") + path


def absolutize(src):
    """Root-relative asset and page links, so the same markup works at / and /ro/."""
    src = re.sub(r'(href|src)="(?!https?:|mailto:|#|/)(assets|css|js)/', r'\1="/\2/', src)
    src = re.sub(r'href="index\.html"', 'href="/"', src)
    src = re.sub(r'href="(?!https?:|/)([a-z0-9-]+\.html)(#[^"]*)?"', r'href="/\1\2"', src)
    return src


def to_ro_links(src):
    def fix(m):
        attr, path = m.group(1), m.group(2)
        if path.startswith(("/assets/", "/css/", "/js/", "/ro/")) or path in ("/CNAME",):
            return m.group(0)
        return '%s="/ro%s"' % (attr, path)
    return re.sub(r'(href|action)="(/[^"]*)"', fix, src)


def translate(src, RO):
    def repl(m):
        key = m.group(3)
        if key not in RO:
            raise SystemExit("missing RO string: " + key)
        return m.group(1) + RO[key] + m.group(4)
    # element with data-i18n="key" ... up to its own closing tag (no nested same tag inside)
    src = re.sub(r'(<(\w+)\b[^>]*\bdata-i18n="([^"]+)"[^>]*>).*?(</\2>)', repl, src, flags=re.S)

    def attrs(m):
        tag = m.group(0)
        for pair in m.group(1).split(";"):
            attr, key = pair.split(":")
            tag = re.sub(r'(\s%s=")[^"]*(")' % re.escape(attr), lambda mm: mm.group(1) + html.escape(RO[key], quote=True) + mm.group(2), tag)
        return tag
    src = re.sub(r'<[^>]*\bdata-i18n-attr="([^"]+)"[^>]*>', attrs, src)
    return src


def text(s):
    return re.sub(r"<[^>]+>", " ", s).replace("  ", " ").strip()


def jsonld(lang, file, title, desc, V):
    org = {
        "@type": "Organization", "@id": SITE + "/#organization", "name": "Visto Apps", "url": SITE + "/",
        "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo/visto-v.png"},
        "email": V["email"],
        "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": V["email"], "availableLanguage": ["English", "Romanian"]},
        "sameAs": [a["site"] for a in V["apps"]],
    }
    website = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Visto Apps",
               "publisher": {"@id": SITE + "/#organization"}, "inLanguage": ["en", "ro"]}
    kind = {"about.html": "AboutPage", "contact.html": "ContactPage", "apps.html": "CollectionPage"}.get(file, "WebPage")
    webpage = {"@type": kind, "@id": url_for(lang, file) + "#webpage", "url": url_for(lang, file), "name": title,
               "description": desc, "inLanguage": lang, "isPartOf": {"@id": SITE + "/#website"},
               "about": {"@id": SITE + "/#organization"}}
    graph = [org, website, webpage]
    if file != "index.html":
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Visto Apps", "item": url_for(lang, "index.html")},
            {"@type": "ListItem", "position": 2, "name": title.split(" | ")[0], "item": url_for(lang, file)}]})
    if file in ("index.html", "apps.html"):
        items = []
        for i, a in enumerate(V["apps"], 1):
            items.append({"@type": "ListItem", "position": i, "item": {
                "@type": "SoftwareApplication", "name": a["name"] + ": " + a["subtitle"][lang],
                "description": a["text"][lang], "applicationCategory": SCHEMA_CATEGORY[a["slug"]],
                "operatingSystem": "iOS", "url": a["store"], "image": SITE + "/assets/icons/" + a["slug"] + ".webp",
                "sameAs": a["site"], "publisher": {"@id": SITE + "/#organization"},
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}})
        graph.append({"@type": "ItemList", "name": "Visto Apps", "numberOfItems": len(items), "itemListElement": items})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def seo_block(lang, file, title, desc, V):
    other = "ro" if lang == "en" else "en"
    robots = "noindex,follow" if file == "404.html" else "index,follow,max-image-preview:large"
    lines = ["<!--gen:seo-->"]
    if file != "404.html":
        lines += [
            '<link rel="canonical" href="%s">' % url_for(lang, file),
            '<link rel="alternate" hreflang="en" href="%s">' % url_for("en", file),
            '<link rel="alternate" hreflang="ro" href="%s">' % url_for("ro", file),
            '<link rel="alternate" hreflang="x-default" href="%s">' % url_for("en", file),
        ]
    lines += [
        '<meta name="robots" content="%s">' % robots,
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Visto Apps">',
        '<meta property="og:title" content="%s">' % html.escape(title, quote=True),
        '<meta property="og:description" content="%s">' % html.escape(desc, quote=True),
        '<meta property="og:url" content="%s">' % url_for(lang, file),
        '<meta property="og:image" content="%s">' % OG_IMAGE,
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="Visto Apps">',
        '<meta property="og:locale" content="%s">' % LOCALES[lang],
        '<meta property="og:locale:alternate" content="%s">' % LOCALES[other],
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % html.escape(title, quote=True),
        '<meta name="twitter:description" content="%s">' % html.escape(desc, quote=True),
        '<meta name="twitter:image" content="%s">' % OG_IMAGE,
    ]
    if file != "404.html":
        lines.append('<script type="application/ld+json">%s</script>' % jsonld(lang, file, title, desc, V))
    lines.append("<!--/gen:seo-->")
    return "\n  " + "\n  ".join(lines)


def legal_table(kind, lang, V, RO):
    def s(key, en):
        return RO[key] if lang == "ro" else en
    rows = []
    for a in V["apps"]:
        link = a["privacy"] if kind == "privacy" else a["terms"]
        label = s("legal.privacy", "Privacy Policy") if kind == "privacy" else s("legal.terms", "Terms of Use")
        site = a["site"].replace("https://", "").rstrip("/")
        rows.append(
            '<tr><th scope="row">%s</th><td><a href="%s" rel="noopener">%s</a></td><td><a href="%s" rel="noopener">%s</a></td></tr>'
            % (html.escape(a["name"]), a["site"], site, link, label))
    out = ['<div class="legal-table-wrap"><table class="legal-table"><thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>'
           % (s("legal.col.app", "App"), s("legal.col.site", "Website"),
              s("legal.col.privacy", "Privacy") if kind == "privacy" else s("legal.col.terms", "Terms"))]
    out += rows
    out.append("</tbody></table></div>")
    if kind == "terms":
        out.append('<p><a href="%s" rel="noopener">%s</a></p>' % (V["appleEula"], s("legal.eula", "Apple Standard License Agreement (EULA)")))
    out.append('<p>%s <a href="mailto:%s">%s</a>.</p>' % (s("legal.contact", "Questions about these documents? Write to us at"), V["email"], V["email"]))
    return "".join(out)


def fill(src, name, content):
    return re.sub(r"<!--gen:%s-->.*?<!--/gen:%s-->" % (name, name), lambda m: "<!--gen:%s-->%s<!--/gen:%s-->" % (name, content, name), src, flags=re.S)


def build():
    V, RO = load_data()
    (ROOT / "ro").mkdir(exist_ok=True)
    for file in PAGES:
        path = ROOT / file
        src = path.read_text()
        src = GEN_SEO.sub("", src)
        src = OLD_SEO.sub("", src)
        src = absolutize(src)
        name = page_name(file)
        title_en = re.search(r"<title>(.*?)</title>", src, re.S).group(1)
        desc_en = re.search(r'<meta name="description" content="([^"]*)">', src).group(1)
        body_keys = 'data-title-key="meta.%s.title" data-desc-key="meta.%s.desc"' % (name, name)
        src = re.sub(r'<body([^>]*?)\s*data-title-key="[^"]*"(\s*data-desc-key="[^"]*")?', r'<body\1 ' + body_keys, src, 1)

        def finish(s, lang, title, desc):
            s = s.replace('<meta name="theme-color" content="#08112b">', '<meta name="theme-color" content="#08112b">' + seo_block(lang, file, title, desc, V), 1)
            s = fill(s, "legal-privacy", legal_table("privacy", lang, V, RO))
            s = fill(s, "legal-terms", legal_table("terms", lang, V, RO))
            return s

        en = finish(src, "en", title_en, desc_en)
        path.write_text(en)

        title_ro, desc_ro = RO["meta.%s.title" % name], RO["meta.%s.desc" % name]
        ro = translate(src, RO)
        ro = ro.replace('<html lang="en">', '<html lang="ro">', 1)
        ro = re.sub(r"<title>.*?</title>", "<title>%s</title>" % html.escape(title_ro), ro, 1, flags=re.S)
        ro = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % html.escape(desc_ro, quote=True), ro, 1)
        ro = to_ro_links(ro)
        ro = finish(ro, "ro", title_ro, desc_ro)
        (ROOT / "ro" / file).write_text(ro)

    urls = []
    for file in INDEXABLE:
        for lang in ("en", "ro"):
            urls.append(
                "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
                '    <xhtml:link rel="alternate" hreflang="en" href="%s"/>\n'
                '    <xhtml:link rel="alternate" hreflang="ro" href="%s"/>\n'
                '    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>\n  </url>\n'
                % (url_for(lang, file), LASTMOD, url_for("en", file), url_for("ro", file), url_for("en", file)))
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "".join(urls) + "</urlset>\n")
    print("built %d pages x 2 languages" % len(PAGES))


LASTMOD = "2026-11-15"

if __name__ == "__main__":
    build()
