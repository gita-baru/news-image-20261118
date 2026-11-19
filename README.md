# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/gita-baru/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/gita-baru/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Version 3 of an editorial front page that sums up the world's news of Wednesday 18 November 2026 in one image: a UTC timeline, four hero stories with detailed drawn scenes (U.S. strikes on Iran, the Kerch Bridge hit again, Xi and Putin in Shenzhen, Voyager 1 reaching one light-day), a numbered grid of 12 more stories with small scene icons, a world map with numbered dots, 34 more stories, and a date check naming what broke before the day and what was not yet due. Version 3 grows from 40 to 50 stories across 7 regions — the ten new stories are Mozambique's Mondlane trial, Guinea jailing 224 over illegal gold mining, Ethiopia–Eritrea artillery near Badme, Mauritius's December Chagos deadline for the UK, Venezuela's 24-hour union strike, Colombia's Q3 contraction, Peru's Tumbes River red alert, Takaichi's first China visit as Japan's PM, Bangladesh's tear-gassed garment protests, and the divided COP31 draft in Antalya — and the hero and grid illustrations are drawn as fuller scenes. Version 2.1's date discipline is kept: Peltola's Alaska win, Nvidia's Q3 results, Kahana's election as speaker, the Kerch span collapse and the Board of Peace report all happened on Tuesday 17 November, so they stay out of the dated stories and are named in the date check. The image is drawn by `draw.py` (PIL) and `main.ts` copies the finished `entry.png` to the output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=gtstps2t&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
