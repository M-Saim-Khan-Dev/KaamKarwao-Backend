import os
import requests

TASK_SERVICE_URL = os.environ.get("TASK_SERVICE_URL", "http://127.0.0.1:8007")
INTERNAL_SERVICE_SECRET = os.environ.get("INTERNAL_SERVICE_SECRET")

def set_task_worker(task_id, worker_id):
    try:
        response = requests.patch(
            f"{TASK_SERVICE_URL}task_service/internal/{task_id}/set-worker/",
            json={"worker_id": worker_id},
            headers={"X-Internal-Secret": INTERNAL_SERVICE_SECRET},
            timeout=5,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Failed to set worker on task {task_id}: {e}")
        return False