[![News Image](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/lusiana27/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/lusiana27/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# Tuesday 24 November 2026 — The World in One Page

**50 sourced stories, a UTC timeline and a date check — 24 November 2026.**

This entry sums up Tuesday 24 November 2026 in a single 1024x1024 image:
50 numbered stories from 7 regions, each with a source, concrete numbers in
every card, a 6-slot UTC timeline, a numbered world map, and a footer
DATE CHECK that names the big stories deliberately left out because they
broke before 24 November (Nvidia's Huang return, the COP31 collapse and the
CrowdStrike–Zscaler deal all broke on 22–23 November, not on the 24th).

## What's on the page

- Masthead: TUESDAY 24 NOVEMBER 2026, "50 STORIES · 7 REGIONS", per-region counts (Europe 15 · Middle East 9 · Asia 7 · Africa 5 · Americas 12 · Oceania 1 · Space 1)
- UTC timeline: overnight drone barrage → Sanofi's $41bn deal → Asia's rally → the CAS ruling → Gaza → US evening data
- 4 hero cards with drawn illustrations: Sanofi–Insmed $41bn, NATO's space warning, Gaza strikes, Seoul +6.3% / Nikkei +3.9%
- 12 small illustrated cards: Ukraine's Delta system, 96 drones, the Perm refinery strike, the UN on Gaza, Iraq's oilfields, Tiangong, the Alibaba blacklist, measles, the first limb-girdle drug, the Grok lawsuit, the Wall Street rebound, Boca's Copa Sudamericana
- "WHERE IT HAPPENED": a numbered world map with one pin per story and a colour legend per region
- Numbered one-line briefs for stories 17–50, so all 50 stories appear on the page
- DATE CHECK footer listing 7 stories excluded on purpose, with their real dates

## How the stories were chosen

Every story was checked against live reporting dated Tuesday 24 November 2026
(Reuters, BBC, Kyiv Independent, FXStreet, AP via wire summaries and others).
Stories are labelled with the outlet that reported them, and claims that rest
on a single unconfirmed report carry a [CLAIM] tag. Anything that broke
earlier — even the day's biggest headlines — went into the DATE CHECK instead
of the story list, so nothing on the page is dated wrong.

## How to run

```sh
python3 main.py
```

Requires Python 3.13 (compatible) and Pillow. The program draws the image
itself with PIL from story data embedded in the code — no network at runtime,
no copied image. It writes exactly one file, `/output/entry.png`
(PNG, 1024x1024, under 1 MiB), clearing only the contents of `/output`.
Two runs produce byte-identical output.

Referral code: j11vkafs
