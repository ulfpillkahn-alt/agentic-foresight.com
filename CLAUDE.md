# agentic-foresight.com

Satellit im Domain-Cluster von Prof. Dr. Ulf Pillkahn. Erklärt den Begriff
**Agentic Foresight** (JSON-LD: `DefinedTerm`, `@id https://agentic-foresight.com/#term`)
und die drei Hebel Scout → Outlook → Tunnel. Zentren: pillkahn.de (Person),
operation-zukunft.de (Angebot). Verbindlich: `CLUSTER-STANDARD.md` im pillkahn.de-Ordner
(`Meine Ablage/pillkahn-de/`) — vor jeder Änderung lesen.

Auftrag (Original): `../02_prompt_claude-code.md` (liegt bewusst außerhalb des Repos).

## Hosting

GitHub Pages, Repo `ulfpillkahn-alt/agentic-foresight.com`, Branch `main`, Root,
`CNAME` = agentic-foresight.com (ohne www). `git push origin main` = Veröffentlichung.
Alles im Repo ist öffentlich abrufbar, auch diese Datei und `pflege/`.
DNS bei All-Inkl (KAS), Umstellung macht Prof.

## Struktur

| DE | EN |
|---|---|
| `/` | `/en/` |
| `/scout/` | `/en/scout/` |
| `/outlook/` | `/en/outlook/` |
| `/tunnel/` | `/en/tunnel/` |
| `/faq/` | `/en/faq/` |
| `/datenschutz/` | `/en/privacy/` |

Dazu `stats.html` (intern, noindex, unverlinkt), `404.html`, `robots.txt`, `sitemap.xml`,
`llms.txt`, `CNAME`, `.nojekyll`, `favicon.svg`.

## Pflege

```
python3 pflege/seo.py
```

Erzeugt Kopf (title, description, canonical, hreflang, OG, Twitter), den einen
JSON-LD-`@graph`, Navigation (`<!-- kopf -->`), Fuß mit Impressum (`<!-- fuss -->`),
setzt die Figuren aus `pflege/figuren/*.svg` ein (`<!-- figur:NAME -->`) und den
Cache-Buster `?v=`. Wiederholbar, bricht bei Title > 60 / Description > 155 ab.
**Kopf, JSON-LD, Navigation, Fuß und Figuren nie im HTML von Hand ändern** —
Skript bzw. SVG-Datei anpassen und Skript laufen lassen. Titles/Descriptions
stehen in `SEITEN` im Skript. Bei CSS/JS-Änderung `VERSION` hochzählen.

Gestaltung: `designsystem.md`. Bildprompts und Job-IDs: `bildstil.md`.

## Vorschau lokal

macOS lässt den Vorschau-Prozess nicht in den Drive-Ordner: Kopie in den
Scratchpad (`rsync -a --delete --exclude .git ./ <scratch>/vorschau/`) und dort
`python3 -m http.server 8790` starten. Lazy-Bilder lädt Headless-Chrome bei
Ganzseiten-Screenshots nicht — für Screenshots `loading="eager"` in einer Kopie.

## Zähler

`js/track.js` meldet an `https://pillkahn.de/api/af/visits.php` (lokal
`http://127.0.0.1:8783/api/af/visits.php`, `php -S 127.0.0.1:8783`).
Merker `af-besuch` (sessionStorage). Kennungen: `cta-angebot`, `hebel-scout`,
`hebel-outlook`, `hebel-tunnel`, `about-pillkahn`, `about-publikationen`,
`about-oekosystem`, `paper-ssrn`, `sprache-en`, `sprache-de`, `datenschutz`.
Der PHP-Zähler liegt im pillkahn.de-Ordner unter `api/af/` (Upload nur mit Freigabe).

## Checkpoints (Freigabe durch Prof.)

1. Startseite DE + Designsystem → Screenshots 1440/390
2. Alle Seiten DE/EN + Prüfbericht → erst danach GitHub-Repo, Push, Pages
3. Änderungen an pillkahn.de / operation-zukunft.de → Diff, Upload nur nach Freigabe
4. DNS-Anleitung KAS → Live-Prüfung

Regeln: Namensregel „Prof. Dr. Ulf Pillkahn"; keine Zeit-/Kostenangaben ohne Quelle;
keine Kunden, Testimonials, Fallzahlen; Siezen nur im Aufruf-Absatz; Werkzeuge nur
mit dem beschreiben, was auf deren Live-Seiten steht; Zugangsdaten nie in Chat oder Repo.
