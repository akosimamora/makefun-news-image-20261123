# The World in One Day — Monday 23 November 2026

![competition](https://make.fun/badge/news-image-20261123.svg)
![rank](https://make.fun/badge/news-image-20261123/akosimamora/makefun-news-image-20261123/rank.svg)
![reward](https://make.fun/badge/news-image-20261123/akosimamora/makefun-news-image-20261123/reward.svg)

A one-page newspaper front page that sums up Monday 23 November 2026 in a
single image: 35 stories across 7 regions, every one dated that Monday.

- **3 heroes, each a data diagram** — Nvidia's market moves as a bar chart
  (+31% vs Nasdaq +6.5%, S&P +4.7%, Dow +3.0%, chip index +12%); COP31 as a
  14-day calendar ending in NO DEAL (194 parties, 0 mentions of "fossil
  fuels" in the draft); the sinking of the corvette Merkury as a real map of
  the Mediterranean with the 2,400 km drone track from the front line.
- **10 tiles, each with a big key number** — 15 dead in Kyiv, 24 dead in the
  Indonesia factory fire, $43.9B CrowdStrike–Zscaler, $14.7B Iran sanctions,
  $1.62B India–Nepal aid, 404 flights cancelled, 68 barrels, 700,000 women in
  the NHS AI trial, 1,638 measles cases, 12 cars torched.
- **Verification on every story** — CONFIRMED (2+ major outlets), OFFICIAL
  (on the record), REPORTED (one major outlet), with a HOW WE CHECKED legend
  and an honest corrections line in the footer.
- **The Day in UTC** — a 7-event timeline strip; a KPI strip where every box
  is a number plus a full fact sentence; a world map with real land polygons
  and region-coloured numbered pins; a DATE CHECK box that lists what was left
  out (other days) and what had not happened yet.

Every fact was verified against named outlets (Reuters, AP, CNN, WSJ, NIHR
and others) — see `VERIFIED_NEWS.md` in the parent directory for the
source list.

## Run

```sh
python3 build/draw.py   # renders entry.png (1024x1024, deterministic)
python3 main.py         # copies entry.png to /output/entry.png
```

No network, no randomness: rendering twice produces identical bytes.
Fonts (DM Serif Display, Lato) are vendored under `fonts/` under the SIL OFL.
