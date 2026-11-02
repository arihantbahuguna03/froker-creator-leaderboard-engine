"""
Demo creator engagement data for leaderboard engine.
All data is synthetic — no real creator names, IDs, or metrics.
"""

DEMO_CREATORS = [
    {
        "creator_id": "DEMO_CREATOR_001",
        "name": "Creator Alpha",
        "niche": "food",
        "city": "Bangalore",
        "followers": 12400,
        "posts_this_week": [
            {"post_id": "P001", "likes": 340, "comments": 28, "shares": 45, "saves": 62, "reach": 3200},
            {"post_id": "P002", "likes": 210, "comments": 12, "shares": 18, "saves": 31, "reach": 1800},
        ],
        "prev_rank": 3,
    },
    {
        "creator_id": "DEMO_CREATOR_002",
        "name": "Creator Beta",
        "niche": "lifestyle",
        "city": "Bangalore",
        "followers": 8900,
        "posts_this_week": [
            {"post_id": "P003", "likes": 890, "comments": 310, "shares": 12, "saves": 9, "reach": 4100},
            {"post_id": "P004", "likes": 760, "comments": 280, "shares": 8,  "saves": 7, "reach": 3900},
        ],
        "prev_rank": 1,
    },
    {
        "creator_id": "DEMO_CREATOR_003",
        "name": "Creator Gamma",
        "niche": "fashion",
        "city": "Bangalore",
        "followers": 21000,
        "posts_this_week": [
            {"post_id": "P005", "likes": 520, "comments": 44, "shares": 88, "saves": 130, "reach": 6200},
        ],
        "prev_rank": 2,
    },
    {
        "creator_id": "DEMO_CREATOR_004",
        "name": "Creator Delta",
        "niche": "fitness",
        "city": "Bangalore",
        "followers": 5600,
        "posts_this_week": [
            {"post_id": "P006", "likes": 190, "comments": 15, "shares": 22, "saves": 48, "reach": 1400},
            {"post_id": "P007", "likes": 210, "comments": 18, "shares": 25, "saves": 52, "reach": 1600},
            {"post_id": "P008", "likes": 230, "comments": 20, "shares": 30, "saves": 58, "reach": 1750},
        ],
        "prev_rank": 5,
    },
    {
        "creator_id": "DEMO_CREATOR_005",
        "name": "Creator Epsilon",
        "niche": "travel",
        "city": "Bangalore",
        "followers": 15200,
        "posts_this_week": [
            {"post_id": "P009", "likes": 410, "comments": 35, "shares": 60, "saves": 95, "reach": 5100},
        ],
        "prev_rank": 4,
    },
]

# Leaderboard prize pool (demo)
PRIZE_POOL = {
    1: 1000,
    2: 500,
    3: 250,
}

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/DEMO_WEBHOOK_URL"
DAG_OWNER = "demo-owner@demo.com"
