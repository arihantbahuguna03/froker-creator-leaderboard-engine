"""
Leaderboard Scoring Config — Example
======================================
Copy this file to scoring_config.py and fill in your calibrated values.
scoring_config.py is gitignored — this example shows the structure only.

The weights were calibrated against historical engagement data to penalise
bought interactions (likes, comments) and reward genuine intent signals
(shares, saves). Tune them to your platform's engagement patterns.
"""

# ── Engagement quality weights ────────────────────────────────────────────────
# Each metric is weighted by its signal quality (saves/shares = intent signals).
# Values are calibrated — not included in this demo repo.
# Contact demo-owner@demo.com to discuss implementation.
WEIGHTS = {
    "shares":   None,   # highest weight — sharing = strong genuine interest
    "saves":    None,   # high weight — saving = intent to return
    "reach":    None,   # moderate weight
    "likes":    None,   # low weight — easily gamed
    "comments": None,   # low weight — easily gamed
}

# ── Prize pool (₹) per leaderboard rank ──────────────────────────────────────
# Calibrated to the platform's weekly creator incentive budget.
# Not included in this demo repo.
PRIZE_POOL = {
    1: None,
    2: None,
    3: None,
}
