# Creator Leaderboard Engine

Hourly Airflow job that scores all active creators on the platform using a quality-weighted engagement model and posts a Slack digest with Claude-generated rank change analysis.

> Built Aug 2024 – Aug 2025 using Claude 3.5 Sonnet API directly — before MCP and modern agentic tooling existed in production-ready form. All orchestration is raw Airflow + Python.

---

## Problem

The platform rewards its top creators weekly with prize money (Rank 1 → ₹1,000, Rank 2 → ₹500, Rank 3 → ₹250). The original ranking was based on raw like + comment counts — which meant creators who bought fake engagement consistently ranked above genuine creators with real reach and saves.

**Result:** The leaderboard lost trust. Good creators stopped participating. Payout money went to inflated accounts.

---

## Solution

A weighted scoring model that values **quality signals** over vanity metrics:

| Signal | Weight | Why |
|---|---|---|
| Shares | 3× | Voluntary amplification — real reach |
| Saves | 3× | Buying intent, deep engagement |
| Reach | 1× | Actual eyeballs |
| Likes | 0.5× | Easy to fake |
| Comments | 0.5× | Easy to fake |

Score is normalised per 1,000 followers so smaller creators can compete with large accounts.

Claude reads the leaderboard and writes a plain-English digest for the internal team: which creators moved up, which dropped, and anything worth reviewing.

---

## Architecture

```
Airflow (hourly)
    └── PythonOperator
            ├── Pull creator engagement data
            ├── Compute weighted score per creator
            ├── Build ranked leaderboard
            ├── Claude 3.5 Sonnet — explain rank changes
            └── Post Slack digest
```

---

## Files

| File | Description |
|---|---|
| `leaderboard_engine.py` | Core scoring + Claude analysis + Slack post |
| `dag.py` | Airflow DAG — hourly schedule |
| `demo_data.py` | Demo creator profiles and engagement data |
| `requirements.txt` | Dependencies |

---

## Sample Slack Output

```
Creator Leaderboard — Nov 03, 2024

#1 Creator Gamma  ↑1  (score: 1.8234)  🏆 ₹1,000
#2 Creator Alpha  ↑1  (score: 1.4102)  🏆 ₹500
#3 Creator Delta  ↑2  (score: 1.2890)  🏆 ₹250
#4 Creator Epsilon  ↓2  (score: 0.9840)
#5 Creator Beta  ↓2  (score: 0.4120)

Analysis:
• Creator Beta dropped from #1 to #5 despite the highest raw engagement —
  880+ likes across two posts, but shares and saves were near zero, suggesting
  the engagement may not be organic.
• Creator Delta jumped 2 spots on 3 posts with strong saves (58 avg) —
  fitness content is resonating with a buying-intent audience.
• Creator Gamma holds #1 with the highest normalised score — 21K followers
  but saves and shares are proportionally strong.
```

---

## Run locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
python leaderboard_engine.py
```

---

## Design Decisions

| Decision | Reasoning |
|---|---|
| Normalise by followers | Without this, creators with 20K followers always beat creators with 5K — unfair to smaller accounts |
| Weight shares = saves = 3× | Both require active intent. Shares spread reach; saves signal intent to act |
| Claude for analysis, not scoring | Scoring is deterministic and auditable. Claude is used only for the human-readable layer |
| Raw Anthropic SDK | Built Aug 2024 — no stable orchestration framework existed. Direct API gives full control |
