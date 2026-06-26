from pybaseball import statcast, cache
import pandas as pd
cache.enable()
import requests
from tqdm import tqdm
from datetime import datetime
import os

# -----------------------------
# Settings
# -----------------------------

START_YEAR = 2008
END_YEAR = datetime.now().year

OUTPUT_FOLDER = "statcast_data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# MLB team IDs (Stats API)
TEAM_IDS = {
    "ARI": 109, "ATL": 144, "BAL": 110, "BOS": 111, "CHC": 112,
    "CWS": 145, "CIN": 113, "CLE": 114, "COL": 115, "DET": 116,
    "HOU": 117, "KC":  118, "LAA": 108, "LAD": 119, "MIA": 146,
    "MIL": 158, "MIN": 142, "NYM": 121, "NYY": 147, "OAK": 133,
    "PHI": 143, "PIT": 134, "SD":  135, "SEA": 136, "SF":  137,
    "STL": 138, "TB":  139, "TEX": 140, "TOR": 141, "WSH": 120,
}

# -----------------------------
# Step 1: Roster / jersey numbers
# -----------------------------

ROSTER_CACHE = os.path.join(OUTPUT_FOLDER, "rosters.parquet")

if os.path.exists(ROSTER_CACHE):
    print("Loading cached roster data...")
    rosters = pd.read_parquet(ROSTER_CACHE)
else:
    print("Downloading roster information from MLB Stats API...")

    roster_rows = []

    for year in range(START_YEAR, END_YEAR + 1):
        for abbrev, team_id in tqdm(TEAM_IDS.items(), desc=f"Season {year}"):
            try:
                url = (
                    "https://statsapi.mlb.com/api/v1/teams/"
                    f"{team_id}/roster"
                    f"?season={year}&rosterType=fullRoster"
                )
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                data = resp.json()

                for player in data.get("roster", []):
                    mlbam_id = player["person"]["id"]
                    name = player["person"]["fullName"]
                    jersey = player.get("jerseyNumber", "")

                    if jersey == "":
                        continue

                    roster_rows.append({
                        "pitcher": mlbam_id,
                        "player_name": name,
                        "jersey_number": int(jersey),
                        "season": year,
                        "team": abbrev,
                    })

            except Exception:
                pass

    rosters = pd.DataFrame(roster_rows).drop_duplicates(
        subset=["pitcher", "season"], keep="first"
    )
    rosters.to_parquet(ROSTER_CACHE)

print(f"Roster entries: {len(rosters):,}")

# Build a lookup dict keyed by (pitcher_id, season) for fast per-row access
roster_lookup = rosters.set_index(["pitcher", "season"])[
    ["jersey_number", "player_name"]
].to_dict("index")

# -----------------------------
# Step 2: Download Statcast (cached per year)
# -----------------------------

STATCAST_COLS = ["pitcher", "release_speed"]

match_counts: dict[tuple, dict] = {}

for year in range(START_YEAR, END_YEAR + 1):
    cache_file = os.path.join(OUTPUT_FOLDER, f"statcast_{year}.parquet")

    if os.path.exists(cache_file):
        print(f"Processing {year} from cache...")
        df = pd.read_parquet(cache_file, columns=STATCAST_COLS)
    else:
        print(f"Downloading {year} Statcast data...")
        df = statcast(f"{year}-03-01", f"{year}-11-30")
        df["season"] = year
        df.to_parquet(cache_file)
        df = df[STATCAST_COLS]

    # -----------------------------
    # Step 3: Find matches for this year
    # -----------------------------

    df = df.dropna(subset=["release_speed"])
    df["rounded_speed"] = df["release_speed"].round().astype(int)

    year_roster = rosters[rosters["season"] == year].set_index("pitcher")

    df = df.join(year_roster[["jersey_number", "player_name"]], on="pitcher")
    df = df.dropna(subset=["jersey_number"])
    df["jersey_number"] = df["jersey_number"].astype(int)

    year_matches = df[df["rounded_speed"] == df["jersey_number"]]

    # Accumulate counts — keep only the tiny aggregation, not raw rows
    for (pitcher_id, player_name, jersey), count in (
        year_matches.groupby(["pitcher", "player_name", "jersey_number"])
        .size()
        .items()
    ):
        key = (pitcher_id, player_name, jersey)
        match_counts[key] = match_counts.get(key, 0) + count

    print(f"  {year}: {len(year_matches):,} matching pitches")

# -----------------------------
# Step 4: Leaderboard
# -----------------------------

leaderboard = (
    pd.DataFrame(
        [
            {
                "pitcher": k[0],
                "player_name": k[1],
                "jersey_number": k[2],
                "matching_pitches": v,
            }
            for k, v in match_counts.items()
        ]
    )
    .sort_values("matching_pitches", ascending=False)
    .reset_index(drop=True)
)

print(f"\nTotal matching pitches across all years: {leaderboard['matching_pitches'].sum():,}")
print("\nTop 50\n")
print(leaderboard.head(50).to_string(index=False))

leaderboard.to_csv("matching_speed_leaderboard.csv", index=False)

# -----------------------------
# Step 5: Individual lookup
# -----------------------------

def lookup_pitcher(name):
    result = leaderboard[
        leaderboard["player_name"].str.contains(name, case=False, na=False)
    ]
    print(result.to_string(index=False) if len(result) else "No pitcher found.")


print("\nExample:")
lookup_pitcher("Holton")
