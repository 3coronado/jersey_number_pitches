# Jersey Number Pitches

Which MLB pitcher has thrown the most pitches at the exact speed of their jersey number?

For example: Tyler Holton of the Detroit Tigers wears **#87** — how many **87 mph** pitches has he thrown in his career?

## How it works

1. Pulls full roster data (including jersey numbers) from the MLB Stats API for every team, 2015–present
2. Downloads pitch-by-pitch Statcast data via [pybaseball](https://github.com/jldbc/pybaseball)
3. Rounds each pitch's `release_speed` to the nearest integer and compares it to the pitcher's jersey number that season
4. Ranks pitchers by total career matching pitches

## Leaderboard

*Last updated: June 25, 2026 — covers 2015 through 2025 Statcast data*

| Rank | Pitcher | Jersey # | Matching Pitches |
|------|---------|----------|-----------------|
| 1 | Dylan Cease | 84 | 755 |
| 2 | Luis Cessa | 85 | 554 |
| 3 | Dustin May | 85 | 404 |
| 4 | Phil Maton | 88 | 383 |
| 5 | Tanner Houck | 89 | 315 |
| 6 | Yoendrys Gómez | 94 | 312 |
| 7 | Tyler Rogers | 71 | 289 |
| 8 | Eduard Bazardo | 83 | 276 |
| 9 | Tyler Holton | 87 | 227 |
| 10 | Spencer Strider | 99 | 205 |
| 11 | Tommy Hunter | 96 | 181 |
| 12 | Clarke Schmidt | 86 | 171 |
| 13 | Yimi García | 93 | 170 |
| 14 | Valente Bellozo | 83 | 160 |
| 15 | Danny Young | 81 | 139 |
| 16 | Luis Garcia | 77 | 137 |
| 17 | JP Sears | 92 | 136 |
| 18 | Dalier Hinojosa | 94 | 125 |
| 19 | Lake Bachar | 84 | 124 |
| 20 | Chris Flexen | 77 | 119 |
| 21 | Génesis Cabrera | 92 | 107 |
| 22 | Michael Grove | 78 | 102 |
| 23 | Ryan Thompson | 81 | 99 |
| 24 | Nabil Crismatt | 74 | 82 |
| 25 | Grant Dayton | 75 | 81 |
| 26 | Spenser Watkins | 80 | 78 |
| 27 | Joe Kelly | 99 | 76 |
| 28 | JT Chargois | 84 | 75 |
| 29 | Miguel Yajure | 89 | 72 |
| 30 | Jack Dreyer | 86 | 63 |
| 31 | Trevor Rogers | 95 | 62 |
| 32 | Matt Gage | 93 | 61 |
| 33 | Grant Hartwig | 93 | 61 |
| 34 | Bryan Hoeing | 93 | 53 |
| 35 | Joe Jacques | 78 | 50 |
| 36 | Parker Messick | 77 | 49 |
| 37 | Edwin Uceta | 92 | 49 |
| 38 | Cooper Criswell | 88 | 45 |
| 39 | Jonathan Pintaro | 91 | 42 |
| 40 | Deivi García | 83 | 39 |
| 41 | Sam Long | 73 | 39 |
| 42 | John Curtiss | 84 | 38 |
| 43 | A.J. Griffin | 64 | 37 |
| 44 | Austin Kitchen | 91 | 36 |
| 45 | Merandy Gonzalez | 77 | 34 |
| 46 | Brennan Bernardino | 83 | 32 |
| 47 | Ben Rowen | 71 | 32 |
| 48 | Emmet Sheehan | 80 | 31 |
| 49 | Bryan Hudson | 93 | 29 |
| 50 | Andre Jackson | 94 | 27 |

Full results in [matching_speed_leaderboard.csv](matching_speed_leaderboard.csv).

## Usage

```bash
pip install pybaseball tqdm pandas pyarrow requests
python jersey_number_pitches.py
```

Statcast downloads are cached to `statcast_data/` so subsequent runs skip re-downloading.
