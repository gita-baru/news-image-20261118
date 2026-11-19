# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/gita-baru/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/gita-baru/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Version 2.1 of an editorial front page that sums up the world's news of Wednesday 18 November 2026 in one image: a UTC timeline, four hero stories (U.S. strikes on Iran, the Kerch Bridge hit again, Xi and Putin in Shenzhen, Voyager 1 reaching one light-day), a numbered grid of 12 more stories, a world map, 24 more stories, and a date check naming what broke before the day and what was not yet due. Version 2.1 fixes the dates: Peltola's Alaska win, Nvidia's Q3 results, Kahana's election as speaker and the Kerch span collapse all happened on Tuesday 17 November, so they were replaced with verified 18 November stories (Voyager 1, Anthropic's $81B IPO, the WHO Gaza flood warning, the Fed minutes) and named in the date check. The image is drawn by `draw.py` (PIL) and `main.ts` copies the finished `entry.png` to the output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=gtstps2t&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
