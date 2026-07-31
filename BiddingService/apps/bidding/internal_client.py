import os
import requests
import logging

TASK_SERVICE_URL = os.environ.get("TASK_SERVICE_URL", "http://127.0.0.1:8007/   ")
INTERNAL_SERVICE_SECRET = os.environ.get("INTERNAL_SERVICE_SECRET")
logger = logging.getLogger(__name__)

def set_task_worker(task_id, worker_id):
    logger.info("Assigning task worker through TaskService task_id=%s worker_id=%s", task_id, worker_id)
    try:
        response = requests.patch(
            f"{TASK_SERVICE_URL}task_service/internal/{task_id}/set-worker/",
            json={"worker_id": worker_id},
            headers={"X-Internal-Secret": INTERNAL_SERVICE_SECRET},
            timeout=5,
        )
        response.raise_for_status()
        return True
    except requests.RequestException:
        logger.exception("TaskService worker assignment failed task_id=%s worker_id=%s", task_id, worker_id)
        return False
