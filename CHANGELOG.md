# Changelog agentic-foresight.com

## 21.11.2026 — IndexNow-Schlüsseldatei

- `ca3edc18a4765a429a3d8bb2b720b140.txt` im Wurzelverzeichnis (Inhalt genau der Schlüssel, für Bing/IndexNow). Erstmeldung der Sitemap mit indexnow.sh (Ordner Meine Ablage).
  Die Datei nicht löschen oder umbenennen, sonst lehnt IndexNow künftige Meldungen ab (403).

## 16.11.2026 — Livegang

**Seiten (DE/EN, je 6):** Start, Scout, Outlook, Tunnel, FAQ, Datenschutz/Privacy; dazu
`404.html` (zweisprachig), `stats.html` (intern, noindex), `robots.txt`, `sitemap.xml`
(10 URLs mit hreflang, Datenschutz ausgenommen), `llms.txt`.

**Gestaltung:** dunkles Karoraster, Kreideweiß, Orange `#F0943F` als einziger Akzent;
Space Grotesk, Inter, JetBrains Mono lokal. Die drei Agenten als Higgsfield-Illustrationen
(AVIF/WebP, 560/760/1000 px), OG-Bilder je Sprache lokal gesetzt. Details: `designsystem.md`,
`bildstil.md`.

**SEO/GEO nach Cluster-Standard:** ein JSON-LD-`@graph` je Seite (Person `pillkahn.de/#person`,
Organisation `operation-zukunft.de/#organization`, `DefinedTerm #term`, ScholarlyArticle SSRN,
FAQPage, BreadcrumbList, Article auf den Hebelseiten), Kernsatz wörtlich, sameAs nur
LinkedIn/X/YouTube. Erzeugt von `pflege/seo.py`.

**Zähler:** `js/track.js` → `pillkahn.de/api/af/visits.php` (eine Zählung pro Sitzung, keine
Cookies, keine IPs). Auf pillkahn.de zusätzlich Eintrag in `/oekosystem/`.

**Prüfung vor Livegang:** Nu-Validator 0 Fehler/0 Warnungen (14 Seiten); Lighthouse mobil
Start 97/100/100/100, Outlook 99/100/100/100, EN Tunnel 98/100/100/100; 390 px ohne
Querscroll.

**Hosting:** GitHub Pages (`main`, Root), DNS bei All-Inkl auf die vier GitHub-Adressen,
www als CNAME. Zertifikat Let's Encrypt (bis 14.02.2027, erneuert GitHub selbst),
HTTPS erzwungen seit 17:58.

**Live-Prüfung 17:58:** alle 10 Sitemap-Adressen 200, unbekannte Adresse 404,
http → https und www → ohne www jeweils 301, JSON-LD parst, Testbesuch in `stats.html` gezählt.

**Offen:** AAAA-Einträge (IPv6) optional; SSRN-Link wegen Cloudflare-Schutz nicht
automatisch prüfbar; englischer Kernsatz zur Bestätigung durch Prof.
