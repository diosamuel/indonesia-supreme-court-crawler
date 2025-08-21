from datetime import datetime
from pathlib import Path
import json
import requests

from airflow import DAG
from airflow.decorators import task

# Configuration
DATA_DIR = Path("/opt/airflow/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
FILE_PATH = DATA_DIR / "payload.json"
WEBHOOK_URL = "https://webhook.site/9de2fb36-9ce3-45e0-b86d-2e07d6449cb5"  # Replace with your URL

# Define DAG
with DAG(
    dag_id="file_to_webhook_pipeline",
    start_date=datetime(2025, 1, 1),
    # schedule_interval=None,  # Trigger manually or set cron
    catchup=False,
    tags=["example", "webhook", "files"],
) as dag:

    # 1. Write a file
    @task()
    def write_file():
        data = {
            "event": "horse_performance",
            "timestamp": datetime.utcnow().isoformat(),
            "score": 98,
        }
        FILE_PATH.write_text(json.dumps(data, indent=2))
        return str(FILE_PATH)

    # 2. Read the file
    @task()
    def read_file(path: str):
        content = json.loads(Path(path).read_text())
        print(f"[DEBUG] File content: {content}")
        return content

    # 3. Send to webhook via POST
    @task()
    def send_webhook(payload: dict):
        try:
            resp = requests.post(WEBHOOK_URL, json=payload, timeout=10)
            resp.raise_for_status()
            print(f"[OK] Webhook response: {resp.status_code}")
        except Exception as e:
            raise RuntimeError(f"Webhook failed: {e}")

    # Task dependencies
    file_path = write_file()
    payload = read_file(file_path)
    send_webhook(payload)
