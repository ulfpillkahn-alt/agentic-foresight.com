# Designsystem agentic-foresight.com

Stand: 16.11.2026 · gilt für alle Seiten, DE und EN.
Familie: Cover von *Flipped Foresight* — dunkles Karopapier, weiße Tuschelinie,
Orange als einzige Akzentfarbe. Eigene Ausprägung über Raster, Linie und Orange;
die Schriften kommen aus operation-zukunft.de und halten die Familie zusammen.

## 1. Farben (Tokens in `css/style.css`, `:root`)

| Token | Wert | Verwendung | Kontrast auf `--grund` |
|---|---|---|---|
| `--grund` | `#141516` | Seitenhintergrund (Papier) | — |
| `--flaeche` | `#1B1D1F` | Karten, Tabellenkopf, Impressum | — |
| `--kreide` | `#F2EFE8` | Text, Tuschelinie der Figuren | 15,9 : 1 |
| `--kreide-2` | `#B8B4AA` | Fließtext zweiter Ordnung | 8,8 : 1 |
| `--kreide-3` | `#8F8B82` | Fußnoten, Datumszeilen | 5,4 : 1 (auf `--flaeche` 5,0 : 1) |
| `--orange` | `#F0943F` | einzige Akzentfarbe: Links, Labels, Signalpunkte, Schaltflächen | 7,9 : 1 (AA und AAA) |
| `--raster` | `rgba(242,239,232,.045)` | kleines Karo (24 px) | — |
| `--raster-2` | `rgba(242,239,232,.08)` | großes Karo (120 px) | — |
| `--linie` | `rgba(242,239,232,.22)` | Rahmen, Trennlinien | — |

Schaltfläche: Orange als Fläche, Schrift `--grund` (7,9 : 1).
Keine Verläufe, keine Schatten, keine Stockfotos, keine Emoji-Icons. Das Karo
entsteht aus zwei Linienrastern (`background-image`), nicht aus einem Bild.

## 2. Typografie

| Rolle | Schrift | Schnitt | Größe |
|---|---|---|---|
| H1 | Space Grotesk, Versalien | 700 | `clamp(2.6rem, 8vw, 5.6rem)`, Zeilenhöhe 0,95 |
| H2 | Space Grotesk | 600 | `clamp(1.6rem, 3.6vw, 2.4rem)` |
| H3 | Space Grotesk | 600 | 1,25 rem |
| Fließtext | Inter | 400 / 600 | 1,0625 rem, Zeilenhöhe 1,65, max. 68 Zeichen |
| Lead (Definition) | Inter | 400 | `clamp(1.15rem, 2vw, 1.4rem)` |
| Label, Kennziffern | JetBrains Mono, Versalien | 500 | 0,78 rem, Laufweite .14em |

Eingebunden sind genau drei variable WOFF2-Dateien (Latin), selbst gehostet,
`font-display: swap`; vorgeladen wird nur Space Grotesk (H1).

## 3. Abstände und Raster

- Grundeinheit 8 px; Abstände 0,5 · 1 · 1,5 · 2 · 3 · 5 · 8 rem.
- Inhaltsbreite `--breite: 1120px`, Lesespalte `--lese: 44rem`.
- Seitenrand `clamp(1rem, 4vw, 2.5rem)` (mobil 16 px).
- Sektionen: `padding-block: clamp(4rem, 9vw, 7.5rem)`, getrennt durch eine
  Haarlinie mit Kennziffer (`01 /`, `02 /` …) — wie die Bemaßung einer Skizze.
- Karo: 24 px fein, 120 px grob; Figuren und Karten sitzen auf dem Raster.

## 4. Komponenten

| Komponente | Klasse | Kurzbeschreibung |
|---|---|---|
| Kopf | `.kopf` | Wortmarke links, Navigation Scout · Outlook · Tunnel · FAQ, Sprachumschalter |
| Label | `.label` | Mono, Orange, mit Kennziffer: `02 / Die drei Hebel` |
| Agentenkette | `.kette` | drei Figuren (inline SVG) + zwei Fluss-Verbinder, jede Figur ein Link |
| Hebelkarte | `.hebel` | Rahmen `--linie`, Eckmarken wie Passermarken, kleine Figur, Text, Link |
| Vergleichstabelle | `.vergleich` | Linien statt Flächen; letzte Spalte (agentisch) mit Orange markiert |
| Arbeitsteilung | `.teilung` | zwei Spalten „Agent übernimmt / Mensch entscheidet" |
| Bänder | `.baender` | Denkfigur Stabil / Veränderung / Neu, ohne Zahlen |
| Aufruf | `.aufruf` | Schaltfläche Orange, ein Absatz in Sie-Form |
| About | `.about` | Porträt 280 px, Kernsatz, drei Links auf pillkahn.de |
| Fuß | `.fuss` | Cluster-Hinweis, Datenschutz, Impressum-Toggle |

## 5. Figuren (inline SVG)

- Quelle: `pflege/figuren/*.svg`; `pflege/seo.py` setzt sie zwischen
  `<!-- figur:NAME -->` und `<!-- /figur -->` ein. Nie im HTML von Hand ändern.
- Einheitlicher Strich: 1,6 px, `vector-effect: non-scaling-stroke`, runde Enden.
  Groß auf der Startseite und klein auf den Hebelseiten bleibt die Linie gleich stark.
- Kreide für Konstruktion und Figuren, Orange nur für Signale, Linse des
  Agenten, Fokus (Matrixfelder, Windkanal-Turbulenz).
- Die Agenten tragen dieselbe Gestalt: Kopf mit orangem Auge, Antenne, Rumpf.
- Bewegung nur CSS (gestrichelter Fluss, pulsierende Signale), bei
  `prefers-reduced-motion: reduce` vollständig aus.

## 6. Bilder

AVIF/WebP mit festen Maßen, unterhalb der ersten Ansicht `loading="lazy"`.
OG-Bild 1200 × 630 je Sprache, aus SVG gerendert (siehe `bildstil.md`).
