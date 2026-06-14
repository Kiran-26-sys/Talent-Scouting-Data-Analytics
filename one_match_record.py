import os
import json

# Correct folder path
json_path = "data_raw/cricsheet_json/cricsheet_json/all_json"

files = os.listdir(json_path)

# Pick first file
sample_file = os.path.join(json_path, files[0])

print("Opening file:", sample_file)

with open(sample_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Check structure
print("Top level keys:", data.keys())
print("Match date:", data["info"]["dates"])
print("Teams:", data["info"]["teams"])


# ---- Extract deliveries from ONE match ----
records = []

match_id = files[0].replace(".json", "")
year = data["info"]["dates"][0].split("-")[0]

for inning in data["innings"]:

    team_data = inning   # inning itself contains team + overs

    for over in team_data["overs"]:
        for delivery in over["deliveries"]:

            batter = delivery["batter"]
            bowler = delivery["bowler"]
            runs = delivery["runs"]["batter"]

            records.append({
                "match_id": match_id,
                "year": year,
                "batter": batter,
                "bowler": bowler,
                "runs": runs
            })

print("Total deliveries extracted:", len(records))
print(records[:5])

#DataFrame creation
import pandas as pd

df = pd.DataFrame(records)

print("\nDataFrame Preview:")
print(df.head())

print("\nShape of DataFrame:", df.shape)

# ---- Scouting Metric 1: Runs per Batter in this match ----

player_runs = df.groupby("batter")["runs"].sum().reset_index()

# sort highest runs first
player_runs = player_runs.sort_values(by="runs", ascending=False)

print("\nRuns per player:")
print(player_runs.head(10))


# ---- Scouting Metric 2: Runs per Player per Year ----

player_year_runs = (
    df.groupby(["year", "batter"])["runs"]
    .sum()
    .reset_index()
)

# sort by runs
player_year_runs = player_year_runs.sort_values(by="runs", ascending=False)

print("\nRuns per player per year:")
print(player_year_runs.head(10))

