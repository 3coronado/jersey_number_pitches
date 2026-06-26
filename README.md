# Jersey Number Pitches

Which MLB pitcher has thrown the most pitches at the exact speed of their jersey number?

For example: Tyler Holton of the Detroit Tigers wears **#87** — how many **87 mph** pitches has he thrown in his career?

## How it works

1. Pulls full roster data (including jersey numbers) from the MLB Stats API for every team, 2008–present
2. Downloads pitch-by-pitch data via [pybaseball](https://github.com/jldbc/pybaseball), covering the full PITCHf/x and Statcast era (2008–present)
3. Rounds each pitch's `release_speed` to the nearest integer and compares it to the pitcher's jersey number that season
4. Ranks pitchers by total career matching pitches

Jersey numbers are matched per season, so a pitcher who changed numbers mid-career only gets credit for pitches thrown at the speed matching their number that year.

## Leaderboard

*Last updated: June 25, 2026 — covers 2008 through 2026 (full pitch tracking era)*

| Rank | Pitcher | Jersey # | Matching Pitches |
|------|---------|----------|-----------------|
| 1 | Dylan Cease | 84 | 755 |
| 2 | Barry Zito | 75 | 727 |
| 3 | Luis Cessa | 85 | 554 |
| 4 | Alfredo Aceves | 91 | 464 |
| 5 | Dustin May | 85 | 404 |
| 6 | Phil Maton | 88 | 383 |
| 7 | Tanner Houck | 89 | 315 |
| 8 | Yoendrys Gómez | 94 | 312 |
| 9 | Tyler Rogers | 71 | 289 |
| 10 | Eduard Bazardo | 83 | 276 |
| 11 | Tyler Holton | 87 | 227 |
| 12 | Spencer Strider | 99 | 205 |
| 13 | Tommy Hunter | 96 | 181 |
| 14 | Clarke Schmidt | 86 | 171 |
| 15 | Yimi García | 93 | 170 |
| 16 | Valente Bellozo | 83 | 160 |
| 17 | Danny Young | 81 | 139 |
| 18 | Luis Garcia | 77 | 137 |
| 19 | JP Sears | 92 | 136 |
| 20 | Dalier Hinojosa | 94 | 125 |
| 21 | Lake Bachar | 84 | 124 |
| 22 | Chris Flexen | 77 | 119 |
| 23 | Génesis Cabrera | 92 | 107 |
| 24 | Michael Grove | 78 | 102 |
| 25 | Ryan Thompson | 81 | 99 |
| 26 | Nabil Crismatt | 74 | 82 |
| 27 | D.J. Carrasco | 77 | 81 |
| 28 | Grant Dayton | 75 | 81 |
| 29 | Spenser Watkins | 80 | 78 |
| 30 | Joe Kelly | 99 | 76 |
| 31 | JT Chargois | 84 | 75 |
| 32 | Miguel Yajure | 89 | 72 |
| 33 | Jack Dreyer | 86 | 63 |
| 34 | Trevor Rogers | 95 | 62 |
| 35 | Matt Gage | 93 | 61 |
| 36 | Grant Hartwig | 93 | 61 |
| 37 | Bryan Hoeing | 93 | 53 |
| 38 | Joe Jacques | 78 | 50 |
| 39 | Edwin Uceta | 92 | 49 |
| 40 | Parker Messick | 77 | 49 |
| 41 | Cooper Criswell | 88 | 45 |
| 42 | Josh Outman | 88 | 43 |
| 43 | Jonathan Pintaro | 91 | 42 |
| 44 | Deivi García | 83 | 39 |
| 45 | Sam Long | 73 | 39 |
| 46 | John Curtiss | 84 | 38 |
| 47 | A.J. Griffin | 64 | 37 |
| 48 | Austin Kitchen | 91 | 36 |
| 49 | Merandy Gonzalez | 77 | 34 |
| 50 | Livan Hernandez | 61 | 33 |

Full results in [matching_speed_leaderboard.csv](matching_speed_leaderboard.csv).

## Usage

```bash
pip install pybaseball tqdm pandas pyarrow requests
python jersey_number_pitches.py
```

Statcast/PITCHf/x downloads are cached to `statcast_data/` so subsequent runs skip re-downloading.
