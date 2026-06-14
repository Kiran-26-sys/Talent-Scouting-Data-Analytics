"""
====================================================
🏏 Indian Cricket Scouting Analytics Pipeline
====================================================

Steps:
1️⃣ Load JSON match files
2️⃣ Extract Indian player deliveries
3️⃣ Aggregate yearly player stats (optimized)
4️⃣ Compute advanced scouting metrics
5️⃣ Data cleaning
6️⃣ Player role classification
7️⃣ Save final scouting dataset
====================================================
"""

import os
import json
import pandas as pd
import numpy as np
from collections import defaultdict

# ==================================================
# 1️⃣ PATH CONFIGURATION
# ==================================================

json_path = "data_raw/cricsheet_json/cricsheet_json/all_json"
files = os.listdir(json_path)

print("Total JSON files to process:", len(files))

# ==================================================
# 2️⃣ AGGREGATION STORAGE (OPTIMIZED)
# ==================================================

player_year_data = defaultdict(lambda: {
    "total_runs": 0,
    "balls_faced": 0,
    "total_boundaries": 0,
    "dot_balls": 0,
    "sum_runs_sq": 0,
    "matches": 0
})

# ==================================================
# 3️⃣ EXTRACT & AGGREGATE DATA (HIGH PERFORMANCE)
# ==================================================

for file in files[:500]:   # increase later to full dataset

    file_path = os.path.join(json_path, file)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        players_info = data.get("info", {}).get("players", {})
        indian_players = players_info.get("India", [])

        year = data["info"]["dates"][0].split("-")[0]

        # track runs per match for consistency calculation
        match_runs_tracker = defaultdict(int)

        for inning in data.get("innings", []):
            for over in inning.get("overs", []):
                for delivery in over.get("deliveries", []):

                    batter = delivery.get("batter")

                    if batter not in indian_players:
                        continue

                    runs = delivery.get("runs", {}).get("batter", 0)

                    key = (year, batter)

                    player_year_data[key]["total_runs"] += runs
                    player_year_data[key]["balls_faced"] += 1

                    if runs >= 4:
                        player_year_data[key]["total_boundaries"] += 1

                    if runs == 0:
                        player_year_data[key]["dot_balls"] += 1

                    match_runs_tracker[batter] += runs

        # update consistency stats
        for batter, match_runs in match_runs_tracker.items():
            key = (year, batter)
            player_year_data[key]["matches"] += 1
            player_year_data[key]["sum_runs_sq"] += match_runs ** 2

    except Exception as e:
        print("Skipping file:", file, e)

# ==================================================
# 4️⃣ CONVERT TO DATAFRAME
# ==================================================

rows = []

for (year, batter), stats in player_year_data.items():
    rows.append({
        "year": year,
        "batter": batter,
        **stats
    })

player_year_stats = pd.DataFrame(rows)

print("DataFrame Shape:", player_year_stats.shape)

# ==================================================
# 5️⃣ OPTIMIZED CONSISTENCY INDEX
# ==================================================

player_year_stats["mean_runs"] = (
    player_year_stats["total_runs"] /
    player_year_stats["matches"]
)

variance = (
    player_year_stats["sum_runs_sq"] /
    player_year_stats["matches"]
) - (player_year_stats["mean_runs"] ** 2)

player_year_stats["consistency_index"] = (
    player_year_stats["mean_runs"] /
    np.sqrt(variance.replace(0, np.nan))
)

# ==================================================
# 6️⃣ ADVANCED SCOUTING METRICS
# ==================================================

player_year_stats["strike_rate"] = (
    player_year_stats["total_runs"] /
    player_year_stats["balls_faced"]
) * 100

player_year_stats["boundary_percent"] = (
    player_year_stats["total_boundaries"] /
    player_year_stats["balls_faced"]
) * 100

player_year_stats["dot_ball_percent"] = (
    player_year_stats["dot_balls"] /
    player_year_stats["balls_faced"]
) * 100

# ==================================================
# 7️⃣ DATA QUALITY CLEANING
# ==================================================

print("\nBefore Cleaning:", player_year_stats.shape)

player_year_stats = player_year_stats[
    player_year_stats["balls_faced"] >= 20
]

player_year_stats["consistency_index"] = (
    player_year_stats["consistency_index"]
    .replace([float("inf"), -float("inf")], 0)
)

player_year_stats = player_year_stats.fillna(0)

print("After Cleaning:", player_year_stats.shape)

# ==================================================
# 8️⃣ SCOUTING SCORE
# ==================================================

player_year_stats["scouting_score"] = (
    player_year_stats["total_runs"] * 0.4 +
    player_year_stats["strike_rate"] * 0.2 +
    player_year_stats["boundary_percent"] * 0.2 +
    player_year_stats["consistency_index"] * 0.2 -
    player_year_stats["dot_ball_percent"] * 0.1
)

player_year_stats = player_year_stats.sort_values(
    by="scouting_score",
    ascending=False
)

# ==================================================
# 9️⃣ PLAYER ROLE CLASSIFICATION
# ==================================================

def classify_role(row):

    if row["strike_rate"] > 130 and row["boundary_percent"] > 18:
        return "Aggressive Batter"

    elif row["consistency_index"] >= 2 and row["strike_rate"] >= 80:
        return "Anchor Batter"

    elif row["dot_ball_percent"] > 60:
        return "Struggling Batter"

    else:
        return "Balanced Player"

player_year_stats["player_role"] = player_year_stats.apply(classify_role, axis=1)

print("\nTop Scouting Players:")
print(player_year_stats.head(15))

# ==================================================
# 🔟 SAVE FINAL DATASET
# ==================================================

player_year_stats.to_csv(
    "data_processed/player_year_stats.csv",
    index=False
)

print("\nSaved to data_processed/player_year_stats.csv")



# # """
# ====================================================
# 🏏 Indian Cricket Scouting Analytics Pipeline
# OLD VERSION — DataFrame-Based Processing
# ====================================================

# Flow:
# 1️⃣ Extract delivery-level data into records list
# 2️⃣ Convert to DataFrame
# 3️⃣ Perform groupby aggregations
# 4️⃣ Compute scouting metrics
# ====================================================
# """

# import os
# import json
# import pandas as pd

# # ==================================================
# # 1️⃣ PATH CONFIGURATION
# # ==================================================

# json_path = "data_raw/cricsheet_json/cricsheet_json/all_json"
# files = os.listdir(json_path)

# print("Total JSON files to process:", len(files))

# records = []

# # ==================================================
# # 2️⃣ EXTRACT DELIVERY LEVEL DATA
# # ==================================================

# for file in files[:500]:   # limit during testing

#     file_path = os.path.join(json_path, file)

#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         players_info = data.get("info", {}).get("players", {})
#         indian_players = players_info.get("India", [])

#         match_id = file.replace(".json", "")
#         year = data["info"]["dates"][0].split("-")[0]

#         for inning in data.get("innings", []):
#             for over in inning.get("overs", []):
#                 for delivery in over.get("deliveries", []):

#                     batter = delivery.get("batter")

#                     if batter not in indian_players:
#                         continue

#                     runs = delivery.get("runs", {}).get("batter", 0)

#                     is_boundary = 1 if runs >= 4 else 0
#                     is_dot = 1 if runs == 0 else 0

#                     records.append({
#                         "match_id": match_id,
#                         "year": year,
#                         "batter": batter,
#                         "runs": runs,
#                         "is_boundary": is_boundary,
#                         "is_dot": is_dot
#                     })

#     except Exception as e:
#         print("Skipping file:", file, e)

# # ==================================================
# # 3️⃣ CREATE DATAFRAME
# # ==================================================

# df = pd.DataFrame(records)

# print("DataFrame Shape:", df.shape)

# # ==================================================
# # 4️⃣ MATCH LEVEL RUNS (FOR CONSISTENCY)
# # ==================================================

# player_match_runs = (
#     df.groupby(["year", "match_id", "batter"])["runs"]
#     .sum()
#     .reset_index()
# )

# # ==================================================
# # 5️⃣ YEARLY PLAYER PERFORMANCE
# # ==================================================

# player_year_stats = (
#     df.groupby(["year", "batter"])
#     .agg(
#         total_runs=("runs", "sum"),
#         balls_faced=("runs", "size"),
#         total_boundaries=("is_boundary", "sum"),
#         dot_balls=("is_dot", "sum")
#     )
#     .reset_index()
# )

# # ==================================================
# # 6️⃣ CONSISTENCY INDEX (OLD METHOD)
# # ==================================================

# consistency_stats = (
#     player_match_runs.groupby(["year", "batter"])["runs"]
#     .agg(["mean", "std"])
#     .reset_index()
# )

# consistency_stats["consistency_index"] = (
#     consistency_stats["mean"] / consistency_stats["std"]
# )

# player_year_stats = pd.merge(
#     player_year_stats,
#     consistency_stats[["year", "batter", "consistency_index"]],
#     on=["year", "batter"],
#     how="left"
# )

# # ==================================================
# # 7️⃣ ADVANCED METRICS
# # ==================================================

# player_year_stats["strike_rate"] = (
#     player_year_stats["total_runs"] /
#     player_year_stats["balls_faced"]
# ) * 100

# player_year_stats["boundary_percent"] = (
#     player_year_stats["total_boundaries"] /
#     player_year_stats["balls_faced"]
# ) * 100

# player_year_stats["dot_ball_percent"] = (
#     player_year_stats["dot_balls"] /
#     player_year_stats["balls_faced"]
# ) * 100

# # ==================================================
# # 8️⃣ DATA CLEANING
# # ==================================================

# player_year_stats = player_year_stats[
#     player_year_stats["balls_faced"] >= 20
# ]

# player_year_stats["consistency_index"] = (
#     player_year_stats["consistency_index"]
#     .replace([float("inf"), -float("inf")], 0)
# )

# player_year_stats = player_year_stats.fillna(0)

# # ==================================================
# # 9️⃣ SCOUTING SCORE
# # ==================================================

# player_year_stats["scouting_score"] = (
#     player_year_stats["total_runs"] * 0.4 +
#     player_year_stats["strike_rate"] * 0.2 +
#     player_year_stats["boundary_percent"] * 0.2 +
#     player_year_stats["consistency_index"] * 0.2 -
#     player_year_stats["dot_ball_percent"] * 0.1
# )

# # ==================================================
# # 🔟 PLAYER ROLE CLASSIFICATION
# # ==================================================

# def classify_role(row):

#     if row["strike_rate"] > 130 and row["boundary_percent"] > 18:
#         return "Aggressive Batter"

#     elif row["consistency_index"] >= 2 and row["strike_rate"] >= 80:
#         return "Anchor Batter"

#     elif row["dot_ball_percent"] > 60:
#         return "Struggling Batter"

#     else:
#         return "Balanced Player"

# player_year_stats["player_role"] = player_year_stats.apply(classify_role, axis=1)

# # ==================================================
# # 1️⃣1️⃣ SAVE DATASET
# # ==================================================

# player_year_stats.to_csv(
#     "data_processed/player_year_stats_old_pipeline.csv",
#     index=False
# )

# print("\nOLD pipeline dataset saved.")
# #