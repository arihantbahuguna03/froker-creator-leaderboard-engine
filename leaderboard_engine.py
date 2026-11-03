"""
Creator Leaderboard Engine
==================================
Scores creators weekly using a weighted engagement model that values
quality signals (shares, saves) over vanity metrics (likes, comments).

Built Aug 2024 – Aug 2025 using raw Anthropic SDK + Airflow.
No LLM orchestration frameworks — direct API calls only.

Problem:
  Raw engagement counts let creators with bought likes dominate the
  leaderboard. Genuine creators with strong saves/shares lose out on
  prize money to inflated accounts.

Solution:
  Weighted scoring: shares (3x) + saves (3x) + reach (1x) + likes (0.5x)
  + comments (0.5x) — normalised per follower. Claude explains each
  creator's rank shift in plain English for the internal team.
"""

import json
import os
from datetime import datetime

import anthropic
import requests

from demo_data import DEMO_CREATORS, SLACK_WEBHOOK_URL


def _load_scoring_config() -> tuple[dict, dict]:
    """
    Load engagement quality weights and prize pool from scoring_config.py.

    WEIGHTS penalise bought interactions (likes, comments) and reward genuine
    intent signals (shares, saves) — calibrated against historical engagement
    data. PRIZE_POOL maps leaderboard rank to ₹ payout.

    Implementation: proprietary — available on request.
    Copy scoring_config.example.py → scoring_config.py to run with your own values.
    """
    try:
        import scoring_config
        return scoring_config.WEIGHTS, scoring_config.PRIZE_POOL
    except ImportError:
        raise RuntimeError(
            "scoring_config.py not found. "
            "Copy scoring_config.example.py → scoring_config.py and fill in your values."
        )


WEIGHTS, PRIZE_POOL = _load_scoring_config()


# ── Scoring ──────────────────────────────────────────────────────────────────

def score_post(post: dict) -> float:
    raw = sum(WEIGHTS[k] * post.get(k, 0) for k in WEIGHTS)
    return round(raw, 2)


def score_creator(creator: dict) -> float:
    posts = creator.get("posts_this_week", [])
    if not posts:
        return 0.0
    total = sum(score_post(p) for p in posts)
    # Normalise by follower count so large accounts don't auto-win
    per_follower = total / max(creator["followers"], 1) * 1000
    return round(per_follower, 4)


def build_leaderboard(creators: list[dict]) -> list[dict]:
    scored = []
    for c in creators:
        score = score_creator(c)
        scored.append({
            "creator_id":   c["creator_id"],
            "name":         c["name"],
            "score":        score,
            "prev_rank":    c.get("prev_rank"),
            "followers":    c["followers"],
            "posts_count":  len(c.get("posts_this_week", [])),
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    for i, entry in enumerate(scored, start=1):
        entry["rank"] = i
        entry["rank_change"] = (entry["prev_rank"] or i) - i
    return scored


# ── Claude explanation ────────────────────────────────────────────────────────

def explain_leaderboard(leaderboard: list[dict]) -> str:
    client = anthropic.Anthropic()

    board_text = "\n".join(
        f"Rank {e['rank']} (was {e['prev_rank']}): {e['name']} — "
        f"score {e['score']}, {e['posts_count']} post(s) this week, "
        f"{e['followers']} followers, "
        f"rank change: {'↑' if e['rank_change'] > 0 else '↓' if e['rank_change'] < 0 else '='}"
        f"{abs(e['rank_change'])}"
        for e in leaderboard
    )

    prompt = f"""You are an analyst for a creator rewards platform.
Below is this week's creator leaderboard with rank changes.

Leaderboard:
{board_text}

Write a short internal digest (3–5 bullet points) explaining the notable rank
changes. Be specific: name the creators, say why they moved up or down based
on the data, and flag anything worth the team reviewing. Keep it under 150 words."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


# ── Prize allocation ──────────────────────────────────────────────────────────

def allocate_prizes(leaderboard: list[dict]) -> list[dict]:
    results = []
    for entry in leaderboard:
        prize = PRIZE_POOL.get(entry["rank"], 0)
        results.append({**entry, "prize_inr": prize})
    return results


# ── Slack ─────────────────────────────────────────────────────────────────────

def post_to_slack(leaderboard: list[dict], explanation: str) -> None:
    lines = [f"*Weekly Creator Leaderboard — {datetime.now().strftime('%b %d, %Y')}*\n"]

    for e in leaderboard[:5]:
        arrow = "↑" if e["rank_change"] > 0 else ("↓" if e["rank_change"] < 0 else "→")
        prize_str = f"  🏆 ₹{e['prize_inr']}" if e.get("prize_inr") else ""
        lines.append(
            f"*#{e['rank']}* {e['name']}  {arrow}{abs(e['rank_change'])}  "
            f"(score: {e['score']}){prize_str}"
        )

    lines.append(f"\n*Analysis:*\n{explanation}")

    payload = {"text": "\n".join(lines)}
    resp = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
    resp.raise_for_status()
    print("Slack message posted.")


# ── Main ──────────────────────────────────────────────────────────────────────

def run_leaderboard_engine(creators: list[dict] | None = None) -> list[dict]:
    from demo_data import DEMO_CREATORS as _default
    creators = creators or _default

    print("Scoring creators…")
    leaderboard = build_leaderboard(creators)
    leaderboard = allocate_prizes(leaderboard)

    print("\nLeaderboard:")
    for e in leaderboard:
        print(
            f"  #{e['rank']} {e['name']}  score={e['score']}  "
            f"prize=₹{e.get('prize_inr', 0)}"
        )

    print("\nAsking Claude for analysis…")
    explanation = explain_leaderboard(leaderboard)
    print(f"\n{explanation}\n")

    if os.getenv("SLACK_ENABLED", "false").lower() == "true":
        post_to_slack(leaderboard, explanation)

    return leaderboard


if __name__ == "__main__":
    run_leaderboard_engine()
