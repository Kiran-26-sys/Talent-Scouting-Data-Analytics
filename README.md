🏏 Indian Cricket Scouting Analytics System

📌 Project Overview

The **Indian Cricket Scouting Analytics System** is a data analytics project designed to identify and evaluate Indian cricket talent using historical ball-by-ball match data from Cricsheet.

The system processes thousands of cricket match JSON files, extracts player performance data, calculates advanced scouting metrics, and generates a ranked scouting dataset that can be used by selectors, analysts, and scouting teams.

This project demonstrates an end-to-end analytics pipeline involving:

* Python Data Engineering
* Data Cleaning & Transformation
* Feature Engineering
* Advanced Sports Analytics
* SQL Integration (Upcoming)
* Power BI Dashboarding (Upcoming)

---
🎯 Business Problem

Scouting teams often face challenges in evaluating players consistently across multiple seasons and competitions.

This project aims to:

* Analyze yearly player performance
* Identify player strengths and weaknesses
* Rank players using a scouting score
* Classify players into batting roles
* Provide a data-driven approach for talent identification

---

📂 Project Structure

```text
Indian-Cricket-Scouting/
│
├── data_raw/
│   └── cricsheet_json/
│
├── data_processed/
│   └── player_year_stats.csv
│
├── scripts/
│   └── process_multiple_matches.py
│
├── README.md
│
└── requirements.txt
```

---

📊 Dataset
 Source

Cricsheet Ball-by-Ball Dataset

Official Website:

[https://cricsheet.org/](https://cricsheet.org/)

Dataset contains:

* Match information
* Teams
* Players
* Innings
* Overs
* Deliveries
* Runs
* Wickets
* Extras

---

🛠 Technologies Used

Programming Language

* Python

 Libraries

* Pandas
* NumPy
* JSON
* OS
* Collections (defaultdict)

 Database (Upcoming)

* MySQL

 Visualization (Upcoming)

* Power BI

---

 ⚙️ Data Processing Pipeline

 1. JSON Parsing

Reads thousands of match JSON files from the Cricsheet dataset.

Extracted fields:

* Match ID
* Year
* Batter
* Runs
* Deliveries

---

 2. Indian Player Filtering

Instead of filtering matches, the pipeline extracts only Indian players from each match.

```python
players_info = data.get("info", {}).get("players", {})
indian_players = players_info.get("India", [])
```

---

 3. Feature Engineering

Additional features created:

| Feature          | Description               |
| ---------------- | ------------------------- |
| total_runs       | Total runs scored         |
| balls_faced      | Total balls faced         |
| total_boundaries | Number of fours and sixes |
| dot_balls        | Number of dot balls       |

---

 4. Advanced Scouting Metrics

 Strike Rate

```text
(total_runs / balls_faced) × 100
```

Measures batting aggression.

---

 Boundary Percentage

```text
(total_boundaries / balls_faced) × 100
```

Measures power-hitting ability.

---

 Dot Ball Percentage

```text
(dot_balls / balls_faced) × 100
```

Measures inability to rotate strike.

---

     Consistency Index

```text
Mean Runs / Standard Deviation
```

Measures performance reliability.

---

   🧹 Data Cleaning

The following cleaning operations were performed:

    Remove Low Sample Players

```python
balls_faced >= 20
```

Removes statistically unreliable records.

---

    Handle Missing Values

```python
fillna(0)
```

---

    Handle Infinite Values

```python
replace([inf, -inf], 0)
```

---

   🏆 Scouting Score

A custom weighted scoring model was developed.

    Formula

```text
Scouting Score =
    (Total Runs × 0.4)
  + (Strike Rate × 0.2)
  + (Boundary % × 0.2)
  + (Consistency Index × 0.2)
  - (Dot Ball % × 0.1)
```

Purpose:

* Rank players automatically
* Identify high-potential talent
* Assist scouting decisions

---

   🎭 Player Role Classification

Players are categorized based on their performance profile.

    Aggressive Batter

```text
Strike Rate > 130
Boundary % > 18
```

---

    Anchor Batter

```text
Consistency Index ≥ 2
Strike Rate ≥ 80
```

---

    Struggling Batter

```text
Dot Ball % > 60
```

---

    Balanced Player

Default category.

---

   📁 Final Output

Generated Dataset:

```text
player_year_stats.csv
```

Contains:

| Column            |
| ----------------- |
| year              |
| batter            |
| total_runs        |
| balls_faced       |
| total_boundaries  |
| dot_balls         |
| matches           |
| mean_runs         |
| consistency_index |
| strike_rate       |
| boundary_percent  |
| dot_ball_percent  |
| scouting_score    |
| player_role       |

---

   📈 Future Enhancements

    SQL Integration

* Create scouting database
* Store processed analytics data
* Execute scouting queries

    Power BI Dashboard

Dashboard pages planned:

* Top Indian Players
* Yearly Performance Trends
* Strength vs Weakness Analysis
* Player Role Distribution
* Scouting Score Rankings

    Additional Metrics

* Batting Average
* Boundary Dependency Index
* Match Impact Score
* Form Index
* Performance Trend Analysis

---

   🚀 How to Run

    Clone Repository

```bash
git clone <repository-url>
```

    Install Dependencies

```bash
pip install pandas numpy
```

    Execute Script

```bash
python scripts/process_multiple_matches.py
```

---

   📊 Sample Analytics Questions Answered

* Who are the best-performing Indian batters each year?
* Which players are most consistent?
* Which players score at the highest strike rate?
* Who relies heavily on boundaries?
* Which players struggle against dot-ball pressure?
* Which emerging players deserve scouting attention?

---

   👨‍💻 Author

**Kiran Kumar**

Data Analytics | Python | SQL | Power BI | Sports Analytics

---

   ⭐ Project Status

    Completed

* JSON Parsing
* Data Engineering Pipeline
* Data Cleaning
* Feature Engineering
* Scouting Metrics
* Player Ranking System
* Role Classification

    In Progress

* MySQL Integration
* Power BI Dashboard Development

---

**Built to demonstrate real-world data engineering and sports analytics workflows using Python, SQL, and Power BI.** 🏏📊
