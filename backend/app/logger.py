import json
import logging
import threading
import time
from urllib import request
from urllib.error import URLError

from app.database import settings


logger = logging.getLogger("loki")


def send_loki_log(message: str, level: str = "info", **labels: str) -> None:
    """Send a single structured log line to Loki without blocking the request."""
    payload = {
        "streams": [
            {
                "stream": {"service": "fastapi", "level": level, **labels},
                "values": [[str(time.time_ns()), message]],
            }
        ]
    }

    def push() -> None:
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            f"{settings.LOKI_URL.rstrip('/')}/loki/api/v1/push",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            request.urlopen(req, timeout=2).close()
        except URLError as exc:
            logger.warning("falha ao enviar log para Loki: %s", exc)

    threading.Thread(target=push, daemon=True).start()
