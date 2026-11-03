"""
Airflow DAG — Creator Leaderboard Engine
Runs hourly. Scores all active creators, updates the leaderboard,
posts Slack digest with Claude-generated analysis.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

DAG_ID    = "creator_leaderboard"
DAG_OWNER = "demo-owner@demo.com"

default_args = {
    "owner":            DAG_OWNER,
    "retries":          1,
    "retry_delay":      timedelta(minutes=5),
    "email_on_failure": False,
}

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description="Score creators hourly and post leaderboard digest to Slack",
    schedule="0 * * * *",
    start_date=datetime(2024, 8, 1),
    catchup=False,
    tags=["leaderboard", "creators"],
) as dag:

    def run_engine():
        import os
        os.environ["SLACK_ENABLED"] = "true"
        from leaderboard_engine import run_leaderboard_engine
        from demo_data import DEMO_CREATORS
        run_leaderboard_engine(DEMO_CREATORS)

    score_and_post = PythonOperator(
        task_id="score_creators_and_post_leaderboard",
        python_callable=run_engine,
    )
