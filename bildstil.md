# Bildstil agentic-foresight.com

Stilreferenz: Cover *Flipped Foresight* (Higgsfield-Job `e76238ee-ff53-4304-b96f-4b4d284b1b61`,
im Repo von operation-zukunft.de als `cover-flipped-foresight.jpg`): dunkles Karopapier,
weiße Kreide-/Tuschelinie, technische Konstruktionsskizze, Orange als einzige Akzentfarbe.

## Stand 16.11.2026

Die drei Agenten sind Higgsfield-Illustrationen (Nano Banana Pro, 2k, 5:4, Stilreferenz Cover).
Die ersten SVG-Figuren (Checkpoint 1) sind ersetzt; sie liegen in der Git-Historie.
Das OG-Bild je Sprache wird lokal aus den drei Illustrationen gesetzt (kein KI-Text im Bild).

## Prompts (Kurzfassung; vollständige Prompts im Protokoll unten)

Gemeinsamer Stilblock (an jeden Prompt anhängen):

> hand-drawn technical construction sketch, white chalk ink lines on a dark charcoal
> grid paper background (fine 24 px grid, coarse 120 px grid), single accent colour
> warm orange #F0943F used only for signals, lenses and focus points, consistent line
> weight, no gradients, no photo, no people faces, no text, no logos, generous empty
> space, style of a patent drawing crossed with an engineer's notebook

1. **Scout** — a small friendly robot agent with a rounded head, one orange lens eye and a
   short antenna stands on a lattice lookout tower and looks through a telescope; a dashed
   search-field sector opens towards the sky, orange signal dots of different sizes inside it,
   dimension line along the tower.
2. **Outlook** — the same robot agent at a tilted drafting table with an impact matrix grid,
   three cells filled orange; above it four small scenario panels arranged as a 2 × 2 scenario
   cross with dashed axes.
3. **Tunnel** — a wind tunnel in side view with a three-blade orange fan at the inlet, a stepped
   architectural strategy model on a stand inside, flow lines bending around it, orange
   turbulence behind the model; the robot agent outside takes notes on a clipboard.
4. **OG / Hero** — the three scenes in one horizontal chain Scout → Outlook → Tunnel, connected
   by dashed orange arrows, title area left empty for typesetting.

## Protokoll

| Datum | Zweck | Modell | Job-ID | Ergebnis |
|---|---|---|---|---|
| 16.11.2026 | Scout (Ausguck, Fernrohr, Suchfeld mit Signalen) | nano_banana_pro, Ref. Cover | `f20ac914-1ab7-4020-a19d-438c4baef5e1` | verwendet |
| 16.11.2026 | Outlook, erste Fassung (Papierrand, anderer Roboter) | nano_banana_pro, Ref. Cover | `322ff0ef-2962-4e6b-a60b-5c0882f33bf3` | verworfen |
| 16.11.2026 | Tunnel (Windkanal, Strategiemodell, Turbulenz) | nano_banana_pro, Ref. Cover | `a93e40f3-a7af-4703-b50a-62195fcf6590` | verwendet |
| 16.11.2026 | Outlook, Neufassung ohne Rand im Stil von Scout | nano_banana_pro, Ref. Scout + Outlook 1 | `0b08a37b-4015-4600-ad38-37665cced376` | verwendet |

Vollständige Prompts:

- **Scout:** „Use the reference image ONLY for its visual style (white chalk ink line drawing on dark charcoal grid paper, orange accent, technical construction sketch). Do not copy its text or machine. Scene: a small friendly robot agent with a rounded rectangular head, one glowing orange lens eye and a short antenna stands on a tall lattice lookout tower and looks through a long telescope towards the upper right. A dashed search-field sector opens from the telescope into the sky; inside it a dozen orange signal dots of different sizes, some with faint concentric rings, a few connected by thin dashed lines into small clusters. Small dimension line with end ticks along the tower, faint horizon line with gentle hills at the bottom." + Stilblock
- **Outlook (verworfen):** „… a small friendly robot agent … stands at a tilted drafting table and draws with a pencil. On the drafting board an impact matrix: a square grid of cells, a few cells filled orange, small arrows between some cells. Above and to the right, four small framed scenario panels arranged as a 2 x 2 scenario cross with dashed horizontal and vertical axes …" + Stilblock
- **Outlook (verwendet):** „Redraw the second reference image (robot at a drafting table with an impact matrix and four scenario panels) in exactly the visual style of the first reference image: same flat dark charcoal grid background reaching to all edges, no paper border, no frame, no vignette, same clean white chalk line weight. Replace the robot with the exact robot character from the first reference image … Keep: the drafting board with a square grid matrix, a few cells filled orange with small arrows, the four framed scenario panels arranged as a 2x2 scenario cross with dashed axes (skyline with sun, network of nodes, globe, lone figure at a horizon), dashed curved arrows from the matrix to the panels, a dimension line with end ticks. Single accent colour warm orange #F0943F, no text, no letters, no numbers, no logos, generous empty space."
- **Tunnel:** „… a wind tunnel in side view, a long cylindrical test section on two supports. At the inlet on the left a three-blade fan glowing orange. Inside the tunnel, on a slim stand, a stepped architectural model … White flow lines stream from left to right and bend around the model; directly behind the model the flow breaks into orange turbulent swirls. Outside the tunnel on the right a small friendly robot agent … takes notes on a clipboard. A dimension line with end ticks above the test section." + Stilblock

Hinweis: Higgsfield meldet als ausführendes Modell `nano_banana_2`, angefordert war `nano_banana_pro`.
