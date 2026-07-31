"""HTTP request and response logging for the User service."""
import logging
import time

logger = logging.getLogger("http.request")


class RequestLoggingMiddleware:
    """Log every HTTP request once, without recording request bodies or secrets."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.monotonic()
        try:
            response = self.get_response(request)
        except Exception:
            logger.exception("Unhandled request failure method=%s path=%s", request.method, request.path)
            raise

        elapsed_ms = (time.monotonic() - started_at) * 1000
        message = "HTTP request completed method=%s path=%s status=%s duration_ms=%.2f"
        args = (request.method, request.path, response.status_code, elapsed_ms)
        if response.status_code >= 500:
            logger.error(message, *args)
        elif response.status_code >= 400:
            logger.warning(message, *args)
        else:
            logger.info(message, *args)
        return response
