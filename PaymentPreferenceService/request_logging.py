"""HTTP request and response logging for the PaymentPreference service."""
import logging
import time
logger = logging.getLogger("http.request")
class RequestLoggingMiddleware:
    def __init__(self, get_response): self.get_response = get_response
    def __call__(self, request):
        started_at = time.monotonic()
        try: response = self.get_response(request)
        except Exception:
            logger.exception("Unhandled request failure method=%s path=%s", request.method, request.path); raise
        message = "HTTP request completed method=%s path=%s status=%s duration_ms=%.2f"; args = (request.method, request.path, response.status_code, (time.monotonic() - started_at) * 1000)
        (logger.error if response.status_code >= 500 else logger.warning if response.status_code >= 400 else logger.info)(message, *args)
        return response
