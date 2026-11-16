#!/usr/bin/env python3
"""
pflege/seo.py — Kopf, Strukturdaten, Navigation, Fuß und Figuren für agentic-foresight.com

Setzt den Cluster-Standard um (CLUSTER-STANDARD.md im Repo von pillkahn.de).
Läuft nur lokal; GitHub Pages liefert das fertige statische HTML aus.
Wiederholbar: Ein zweiter Lauf ändert nichts.

Je Seite:
  1. entfernt title, description, canonical, hreflang, robots, og:*, article:*,
     twitter:* und setzt einen vollständigen Block direkt hinter <meta viewport>
  2. ersetzt alle JSON-LD-Blöcke durch EINEN @graph vor </head>
  3. füllt <!-- kopf --> … <!-- /kopf --> (Wortmarke, Navigation, Sprachumschalter)
     und <!-- fuss --> … <!-- /fuss --> (Cluster-Hinweis, Datenschutz, Impressum)
  4. setzt die Figuren aus pflege/figuren/NAME.svg zwischen
     <!-- figur:NAME --> und <!-- /figur --> ein
  5. Cache-Buster ?v= für CSS und JS

Aufruf im Repo-Root:   python3 pflege/seo.py
Bricht ab, wenn ein Title > 60 oder eine Description > 155 Zeichen hat.
"""

import html
import json
import os
import re
import sys

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://agentic-foresight.com"
VERSION = "2026-11-16"          # Cache-Buster für CSS/JS — bei Änderungen hochzählen

# ------------------------------------------------------------------ Kanon
PERSON_ID = "https://pillkahn.de/#person"
ORG_ID = "https://operation-zukunft.de/#organization"
SITE_ID = DOMAIN + "/#website"
TERM_ID = DOMAIN + "/#term"

# Schlanker Personenknoten — der vollständige lebt auf pillkahn.de.
PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": "Ulf Pillkahn",
    "honorificPrefix": "Prof. Dr.",
    "url": "https://pillkahn.de/",
    "sameAs": [  # nur die im Cluster-Standard verifizierten Profile, nie eigene Domains
        "https://www.linkedin.com/in/prof-dr-ulf-pillkahn-1b7a6131/",
        "https://x.com/Ulf_Pillkahn",
        "https://www.youtube.com/@profandprompt",
    ],
}
ORG = {
    "@type": "Organization",
    "@id": ORG_ID,
    "name": "Operation Zukunft",
    "url": "https://operation-zukunft.de/",
    "founder": {"@id": PERSON_ID},
}

TEXT = {
    "de": {
        "lang": "de-DE", "og_locale": "de_DE",
        "site_name": "Agentic Foresight",
        "definition": ("Agentic Foresight ist Foresight-Arbeit, in der spezialisierte KI-Agenten "
                       "Signale suchen, Szenarien bauen und Strategien gegen diese Szenarien prüfen. "
                       "Menschen stellen die Fragen, bewerten und entscheiden."),
        "start": "Start",
        "bild_alt": "Agentic Foresight: die Agenten Scout, Outlook und Tunnel als Konstruktionsskizze",
    },
    "en": {
        "lang": "en", "og_locale": "en_GB",
        "site_name": "Agentic Foresight",
        "definition": ("Agentic Foresight is foresight work in which specialised AI agents search "
                       "for signals, build scenarios and test strategies against them. Humans ask "
                       "the questions, judge and decide."),
        "start": "Home",
        "bild_alt": "Agentic Foresight: the agents Scout, Outlook and Tunnel as a construction sketch",
    },
}

# ------------------------------------------------------------------ Seiten
# Jede Seite einmal je Sprache. "paar" verbindet die Entsprechungen (hreflang,
# Sprachumschalter). Datum: erstellt / zuletzt geändert (sichtbar auf Unterseiten).
SEITEN = [
    {"paar": "start", "art": "start",
     "de": {"datei": "index.html", "pfad": "/",
            "title": "Agentic Foresight: KI-Agenten für Szenarioarbeit",
            "desc": ("Agentic Foresight: KI-Agenten suchen Signale, bauen Szenarien und prüfen "
                     "Strategien. Menschen fragen, bewerten und entscheiden. Methode und Grenzen.")},
     "en": {"datei": "en/index.html", "pfad": "/en/",
            "title": "Agentic Foresight: AI agents for scenario work",
            "desc": ("Agentic Foresight: AI agents search for signals, build scenarios and test "
                     "strategies. Humans ask, judge and decide. Method, roles and limits.")}},
    {"paar": "scout", "art": "hebel", "figur": "scout", "erstellt": "2026-11-16", "geaendert": "2026-11-16",
     "de": {"datei": "scout/index.html", "pfad": "/scout/", "name": "Scout",
            "title": "Scout: Wie KI-Agenten Signale für Szenarien finden",
            "desc": ("Der Scout-Agent durchsucht ein Suchfeld, erfasst Signale mit Belegen und "
                     "schlägt Einflussfaktoren vor. Was er übernimmt, was der Mensch entscheidet.")},
     "en": {"datei": "en/scout/index.html", "pfad": "/en/scout/", "name": "Scout",
            "title": "Scout: how AI agents find signals for scenarios",
            "desc": ("The Scout agent scans a search field, records signals with evidence and "
                     "proposes drivers. What the agent does and what humans decide.")}},
    {"paar": "outlook", "art": "hebel", "figur": "outlook", "erstellt": "2026-11-16", "geaendert": "2026-11-16",
     "de": {"datei": "outlook/index.html", "pfad": "/outlook/", "name": "Outlook",
            "title": "Outlook: Wie KI-Agenten Szenarien nach Lehrbuch bauen",
            "desc": ("Von Einflussfaktoren über Einflussmatrix und Wilson-Matrix zum Szenariorahmen: "
                     "Wie der Outlook-Agent Szenarien baut und wo der Mensch entscheidet.")},
     "en": {"datei": "en/outlook/index.html", "pfad": "/en/outlook/", "name": "Outlook",
            "title": "Outlook: how AI agents build scenarios by the book",
            "desc": ("From drivers via impact matrix and Wilson matrix to the scenario framework: "
                     "how the Outlook agent builds scenarios and where humans decide.")}},
    {"paar": "tunnel", "art": "hebel", "figur": "tunnel", "erstellt": "2026-11-16", "geaendert": "2026-11-16",
     "de": {"datei": "tunnel/index.html", "pfad": "/tunnel/", "name": "Tunnel",
            "title": "Tunnel: Strategien mit KI-Agenten im Windkanal prüfen",
            "desc": ("Strategic Fit: Der Tunnel-Agent prüft die Strategie gegen jedes Szenario, "
                     "zeigt Robustheit und Lücken und leitet Frühwarnindikatoren ab.")},
     "en": {"datei": "en/tunnel/index.html", "pfad": "/en/tunnel/", "name": "Tunnel",
            "title": "Tunnel: testing strategy in a wind tunnel with AI agents",
            "desc": ("Strategic fit: the Tunnel agent tests a strategy against every scenario, "
                     "shows robustness and gaps and derives early-warning indicators.")}},
    {"paar": "faq", "art": "faq", "erstellt": "2026-11-16", "geaendert": "2026-11-16",
     "de": {"datei": "faq/index.html", "pfad": "/faq/", "name": "FAQ",
            "title": "FAQ und Glossar: KI-Agenten und Agentic Foresight",
            "desc": ("Was ist ein KI-Agent, was unterscheidet ihn vom Chatbot, was kann KI beim "
                     "wirklich Neuen nicht? Antworten und Glossar zu Agentic Foresight.")},
     "en": {"datei": "en/faq/index.html", "pfad": "/en/faq/", "name": "FAQ",
            "title": "FAQ and glossary: AI agents and Agentic Foresight",
            "desc": ("What is an AI agent, how does it differ from a chatbot, what can AI not do "
                     "with the genuinely new? Answers and a glossary on Agentic Foresight.")}},
    {"paar": "datenschutz", "art": "rechtlich", "index": False,
     "de": {"datei": "datenschutz/index.html", "pfad": "/datenschutz/", "name": "Datenschutz",
            "title": "Datenschutzerklärung | Agentic Foresight",
            "desc": "Datenschutzerklärung von agentic-foresight.com: Hosting, anonymer Besuchszähler, Schriften, externe Links und Ihre Rechte."},
     "en": {"datei": "en/privacy/index.html", "pfad": "/en/privacy/", "name": "Privacy",
            "title": "Privacy policy | Agentic Foresight",
            "desc": "Privacy policy of agentic-foresight.com: hosting, anonymous visit counter, fonts, external links and your rights."}},
]

# Ohne Paar: nur Fuß/Kopf/Cache-Buster, Kopfblock bleibt wie geschrieben
NUR_RAHMEN = ["404.html", "stats.html"]

# Illustrationen (Higgsfield, siehe bildstil.md). Breite x Höhe der großen Fassung.
BILD_MASS = (1000, 806)
BILD_ALT = {
    "scout": {
        "de": ("Skizze: Ein kleiner Roboter steht auf einem Gitterturm und blickt durch ein Fernrohr "
               "in ein gestricheltes Suchfeld voller orangefarbener Signalpunkte."),
        "en": ("Sketch: a small robot on a lattice tower looks through a telescope into a dashed "
               "search field full of orange signal dots."),
    },
    "outlook": {
        "de": ("Skizze: Ein Roboter zeichnet am Zeichentisch eine Einflussmatrix; gestrichelte Pfeile "
               "führen zu vier Szenariotafeln im Szenariokreuz."),
        "en": ("Sketch: a robot draws an impact matrix at a drafting table; dashed arrows lead to four "
               "scenario panels arranged as a scenario cross."),
    },
    "tunnel": {
        "de": ("Skizze: Windkanal mit orange leuchtendem Gebläse. Die Strömung umfließt ein "
               "stufenförmiges Strategiemodell und wird dahinter turbulent; ein Roboter notiert die Messung."),
        "en": ("Sketch: a wind tunnel with a glowing orange fan. The flow passes a stepped strategy "
               "model and turns turbulent behind it; a robot takes notes."),
    },
}

NAV = {
    "de": [("Scout", "/scout/"), ("Outlook", "/outlook/"), ("Tunnel", "/tunnel/"), ("FAQ", "/faq/")],
    "en": [("Scout", "/en/scout/"), ("Outlook", "/en/outlook/"), ("Tunnel", "/en/tunnel/"), ("FAQ", "/en/faq/")],
}


# ------------------------------------------------------------------ Bausteine
def e(t):
    return html.escape(t, quote=True)


def bild(sprache):
    return {"url": f"{DOMAIN}/img/og-{sprache}.png", "w": 1200, "h": 630,
            "alt": TEXT[sprache]["bild_alt"]}


def kopfblock(s, sp):
    v = s[sp]
    url = DOMAIN + v["pfad"]
    b = bild(sp)
    andere = "en" if sp == "de" else "de"
    z = [f'    <title>{e(v["title"])}</title>',
         f'    <meta name="description" content="{e(v["desc"])}">',
         f'    <meta name="robots" content="{"index, follow" if s.get("index", True) else "noindex, follow"}">',
         f'    <link rel="canonical" href="{url}">',
         f'    <link rel="alternate" hreflang="de" href="{DOMAIN + s["de"]["pfad"]}">',
         f'    <link rel="alternate" hreflang="en" href="{DOMAIN + s["en"]["pfad"]}">',
         f'    <link rel="alternate" hreflang="x-default" href="{DOMAIN + s["de"]["pfad"]}">',
         f'    <meta property="og:type" content="{"article" if s["art"] == "hebel" else "website"}">',
         '    <meta property="og:site_name" content="Agentic Foresight">',
         f'    <meta property="og:locale" content="{TEXT[sp]["og_locale"]}">',
         f'    <meta property="og:locale:alternate" content="{TEXT[andere]["og_locale"]}">',
         f'    <meta property="og:url" content="{url}">',
         f'    <meta property="og:title" content="{e(v["title"])}">',
         f'    <meta property="og:description" content="{e(v["desc"])}">',
         f'    <meta property="og:image" content="{b["url"]}">',
         f'    <meta property="og:image:width" content="{b["w"]}">',
         f'    <meta property="og:image:height" content="{b["h"]}">',
         f'    <meta property="og:image:alt" content="{e(b["alt"])}">']
    if s["art"] == "hebel":
        z.append(f'    <meta property="article:published_time" content="{s["erstellt"]}">')
        z.append(f'    <meta property="article:modified_time" content="{s["geaendert"]}">')
        z.append('    <meta property="article:author" content="https://pillkahn.de/">')
    z += ['    <meta name="twitter:card" content="summary_large_image">',
          '    <meta name="twitter:creator" content="@Ulf_Pillkahn">',
          f'    <meta name="twitter:title" content="{e(v["title"])}">',
          f'    <meta name="twitter:description" content="{e(v["desc"])}">',
          f'    <meta name="twitter:image" content="{b["url"]}">',
          f'    <meta name="twitter:image:alt" content="{e(b["alt"])}">']
    return "\n".join(z)


def faq_paare(t):
    """Fragen und Antworten aus <details class="faq"> lesen (Antwort ohne HTML)."""
    paare = []
    for q, a in re.findall(r'<details class="faq"[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', t, re.S):
        q = html.unescape(re.sub(r"<[^>]+>", "", q)).strip()
        a = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a))).strip()
        a = re.sub(r" ([.,;:!?)])", r"\1", a)
        paare.append((q, a))
    return paare


def graph(s, sp, t):
    v = s[sp]
    url = DOMAIN + v["pfad"]
    lang = TEXT[sp]["lang"]
    site = {
        "@type": "WebSite", "@id": SITE_ID, "url": DOMAIN + "/",
        "name": "Agentic Foresight", "inLanguage": ["de-DE", "en"],
        "about": {"@id": TERM_ID},
        "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID},
    }
    term = {
        "@type": "DefinedTerm", "@id": TERM_ID, "name": "Agentic Foresight",
        "description": TEXT[sp]["definition"], "url": DOMAIN + ("/" if sp == "de" else "/en/"),
        "inLanguage": lang,
        "creator": {"@id": PERSON_ID},
        "subjectOf": {"@id": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7322758"},
    }
    paper = {
        "@type": "ScholarlyArticle", "@id": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7322758",
        "name": "Flipped Foresight", "url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7322758",
        "sameAs": "https://doi.org/10.2139/ssrn.7322758", "author": {"@id": PERSON_ID},
    }
    seite = {
        "@type": "FAQPage" if s["art"] == "faq" else "WebPage",
        "@id": url + "#webpage", "url": url, "name": v["title"], "description": v["desc"],
        "inLanguage": lang, "isPartOf": {"@id": SITE_ID}, "about": {"@id": TERM_ID},
        "breadcrumb": {"@id": url + "#breadcrumb"},
    }
    if "geaendert" in s:
        seite["datePublished"] = s["erstellt"]
        seite["dateModified"] = s["geaendert"]
    start_url = DOMAIN + ("/" if sp == "de" else "/en/")
    krumen = [{"@type": "ListItem", "position": 1, "name": TEXT[sp]["start"], "item": start_url}]
    if s["paar"] != "start":
        krumen.append({"@type": "ListItem", "position": 2, "name": v["name"], "item": url})
    brot = {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": krumen}

    knoten = [PERSON, ORG, site, term, paper, seite, brot]
    if s["art"] == "start":
        seite["mainEntity"] = {"@id": TERM_ID}
    if s["art"] == "hebel":
        h1 = html.unescape(re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S).group(1)))
        knoten.append({
            "@type": "Article", "@id": url + "#article",
            "headline": re.sub(r"\s+", " ", h1).strip(), "description": v["desc"], "url": url,
            "mainEntityOfPage": {"@id": url + "#webpage"}, "isPartOf": {"@id": SITE_ID},
            "about": {"@id": TERM_ID}, "inLanguage": lang,
            "datePublished": s["erstellt"], "dateModified": s["geaendert"],
            "image": bild(sp)["url"],
            "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID},
        })
    if s["art"] == "faq":
        seite["mainEntity"] = [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_paare(t)]
    daten = {"@context": "https://schema.org", "@graph": knoten}
    text = json.dumps(daten, ensure_ascii=False, indent=2)
    text = "\n".join("    " + z for z in text.splitlines())
    return ('    <!-- Strukturdaten: generiert von pflege/seo.py nach dem Cluster-Standard -->\n'
            '    <script type="application/ld+json">\n' + text + '\n    </script>\n')


def kopf_html(sp, aktuell, gegen):
    """Wortmarke, Navigation, Sprachumschalter auf die Entsprechung."""
    start = "/" if sp == "de" else "/en/"
    links = []
    for name, pfad in NAV[sp]:
        cur = ' aria-current="page"' if pfad == aktuell else ""
        links.append(f'      <a href="{pfad}"{cur}>{name}</a>')
    if sp == "de":
        links.append(f'      <a class="sprache" href="{gegen}" hreflang="en" lang="en" data-track="sprache-en">EN</a>')
        label = "Hauptnavigation"
    else:
        links.append(f'      <a class="sprache" href="{gegen}" hreflang="de" lang="de" data-track="sprache-de">DE</a>')
        label = "Main navigation"
    return ('<header class="kopf">\n  <div class="huelle">\n'
            f'    <a class="marke" href="{start}">Agentic<b>·</b>Foresight</a>\n'
            f'    <nav class="nav" aria-label="{label}">\n' + "\n".join(links) +
            '\n    </nav>\n  </div>\n</header>')


IMPRESSUM = {
    "de": ("Impressum", "/datenschutz/", "Datenschutz",
           """      <h2>Impressum</h2>
      <p><strong>Angaben gemäß § 5 DDG</strong></p>
      <p>Prof. Dr. Ulf Pillkahn<br>Maxhofstraße 28<br>81475 München</p>
      <p><strong>Kontakt:</strong> <a href="mailto:info@operation-zukunft.de">info@operation-zukunft.de</a></p>
      <p><strong>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV:</strong><br>Prof. Dr. Ulf Pillkahn</p>
      <p><strong>Haftungsausschluss:</strong> Die Inhalte dieser Seiten wurden mit größter Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte kann jedoch keine Gewähr übernommen werden. Als Diensteanbieter ist Prof. Dr. Ulf Pillkahn gemäß § 7 Abs. 1 DDG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich, nach §§ 8 bis 10 DDG jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen. Für die Inhalte verlinkter externer Seiten sind ausschließlich deren Betreiber verantwortlich.</p>"""),
    "en": ("Legal notice", "/en/privacy/", "Privacy",
           """      <h2>Legal notice</h2>
      <p><strong>Information pursuant to § 5 DDG (German Digital Services Act)</strong></p>
      <p>Prof. Dr. Ulf Pillkahn<br>Maxhofstraße 28<br>81475 München<br>Germany</p>
      <p><strong>Contact:</strong> <a href="mailto:info@operation-zukunft.de">info@operation-zukunft.de</a></p>
      <p><strong>Responsible for content pursuant to § 18 (2) MStV:</strong><br>Prof. Dr. Ulf Pillkahn</p>
      <p><strong>Disclaimer:</strong> The content of these pages has been prepared with great care. No guarantee can be given, however, for its accuracy, completeness or timeliness. As a service provider, Prof. Dr. Ulf Pillkahn is responsible for his own content on these pages under general law in accordance with § 7 (1) DDG, but under §§ 8 to 10 DDG is not obliged to monitor transmitted or stored third-party information or to investigate circumstances indicating illegal activity. The operators of linked external sites are solely responsible for their content. The German version of this legal notice is authoritative.</p>"""),
}


def fuss_html(sp):
    knopf, ds_pfad, ds_name, inhalt = IMPRESSUM[sp]
    hinweis = ("Ein Projekt von" if sp == "de" else "A project by")
    return ('<footer class="fuss">\n  <div class="huelle">\n    <div class="fuss-zeile">\n'
            '      <div class="fuss-links">\n'
            f'        <p class="cluster-hinweis">{hinweis} <a href="https://pillkahn.de/">Prof. Dr. Ulf Pillkahn</a></p>\n'
            f'        <a href="{ds_pfad}" data-track="datenschutz">{ds_name}</a>\n'
            '      </div>\n'
            f'      <button class="impressum-toggle" type="button" aria-expanded="false" aria-controls="impressum" data-text="{knopf}">{knopf} ▼</button>\n'
            '    </div>\n'
            '    <div id="impressum" class="impressum">\n' + inhalt + '\n    </div>\n'
            '    <p class="copy">© 2026 Prof. Dr. Ulf Pillkahn · Operation Zukunft</p>\n'
            '  </div>\n</footer>')


def figuren(t, sp):
    """<!-- figur:NAME[:seite] --> … <!-- /figur -->: Bild als <picture> (AVIF, WebP)."""
    w, h = BILD_MASS
    def ein(m):
        name, kontext = m.group(1), m.group(2) or "kette"
        if kontext == "seite":
            alt = BILD_ALT[name][sp]
            sizes = "(max-width: 900px) 92vw, 470px"
            laden = 'fetchpriority="high"'
        else:
            alt = ""        # in der Kette trägt der Linktext den Namen; Bild ist Schmuck
            sizes = "(max-width: 900px) 90vw, 330px"
            # Kette liegt am Desktop in der ersten Ansicht; Scout ist mobil das LCP-Element
            laden = 'fetchpriority="high"' if name == "scout" else 'loading="eager"'
        quellen = "\n".join(
            f'  <source type="image/{fmt}" srcset="/img/{name}-560.{fmt} 560w, /img/{name}-760.{fmt} 760w, /img/{name}.{fmt} {w}w" sizes="{sizes}">'
            for fmt in ("avif", "webp"))
        bild = (f"<picture>\n{quellen}\n"
                f'  <img src="/img/{name}.webp" alt="{e(alt)}" width="{w}" height="{h}" {laden} decoding="async">\n'
                "</picture>")
        marke = name + (":" + m.group(2) if m.group(2) else "")
        return f"<!-- figur:{marke} -->\n{bild}\n<!-- /figur -->"
    return re.sub(r"<!-- figur:([a-z]+)(?::([a-z]+))? -->.*?<!-- /figur -->", ein, t, flags=re.S)


def rahmen(t, sp, aktuell, gegen):
    t = re.sub(r"<!-- kopf -->.*?<!-- /kopf -->",
               lambda m: "<!-- kopf -->\n" + kopf_html(sp, aktuell, gegen) + "\n<!-- /kopf -->", t, flags=re.S)
    t = re.sub(r"<!-- fuss -->.*?<!-- /fuss -->",
               lambda m: "<!-- fuss -->\n" + fuss_html(sp) + "\n<!-- /fuss -->", t, flags=re.S)
    t = figuren(t, sp)
    t = re.sub(r'((?:style\.css|main\.js|track\.js|stats\.js))\?v=[0-9a-z-]+', r'\1?v=' + VERSION, t)
    return t


# ------------------------------------------------------------------ Lauf
def main():
    zu_lang = []
    for s in SEITEN:
        for sp in ("de", "en"):
            v = s[sp]
            if len(v["title"]) > 60:
                zu_lang.append(f'{v["datei"]}: Title {len(v["title"])}')
            if len(v["desc"]) > 155:
                zu_lang.append(f'{v["datei"]}: Description {len(v["desc"])}')
    if zu_lang:
        sys.exit("Zu lang:\n  " + "\n  ".join(zu_lang))

    fehlend = []
    for s in SEITEN:
        for sp in ("de", "en"):
            v = s[sp]
            p = os.path.join(BASIS, v["datei"])
            if not os.path.exists(p):
                fehlend.append(v["datei"])
                continue
            t = open(p, encoding="utf-8").read()
            kopf, rest = t[:t.index("</head>")], t[t.index("</head>"):]
            for muster in [r"<title>.*?</title>",
                           r'<meta name="(?:description|keywords|author|robots)"[^>]*>',
                           r'<link rel="(?:canonical|alternate)"[^>]*>',
                           r'<meta property="(?:og|article):[^"]*"[^>]*>',
                           r'<meta name="twitter:[^"]*"[^>]*>',
                           r'<!-- Strukturdaten: generiert[^\n]*-->',
                           r'<script type="application/ld\+json">.*?</script>']:
                kopf = re.sub(r"\n?[ \t]*" + muster, "", kopf, flags=re.S)
            vp = re.search(r'<meta name="viewport"[^>]*>', kopf)
            kopf = kopf[:vp.end()] + "\n" + kopfblock(s, sp) + kopf[vp.end():]
            kopf = kopf.rstrip() + "\n" + graph(s, sp, t)
            gegen = s["en" if sp == "de" else "de"]["pfad"]
            t = rahmen(kopf + rest, sp, v["pfad"], gegen)
            open(p, "w", encoding="utf-8").write(t)
            print(f'  {v["datei"]:26s} Title {len(v["title"]):2d}  Desc {len(v["desc"]):3d}')

    for d in NUR_RAHMEN:
        p = os.path.join(BASIS, d)
        if not os.path.exists(p):
            fehlend.append(d)
            continue
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(rahmen(t, "de", "", "/en/"))
        print(f"  {d:26s} nur Rahmen und Cache-Buster")
    if fehlend:
        print("  (noch nicht angelegt: " + ", ".join(fehlend) + ")")


if __name__ == "__main__":
    main()
