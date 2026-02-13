"""
API Request Logging Middleware
Logs every incoming request and outgoing response to logs/api.log
"""
import time
import json
import logging

api_logger = logging.getLogger('api')


class APIRequestLogMiddleware:
    """
    Middleware that logs:
      • Incoming request  — method, path, user, IP, query params
      • Outgoing response — status code, response time (ms)
      • Errors (4xx/5xx)  — includes request body for debugging
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ── Skip admin & static paths (optional, keeps logs clean) ──
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return self.get_response(request)

        start_time = time.time()

        # ── Capture request info ────────────────────────────────────
        method = request.method
        path = request.get_full_path()
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        ip = self._get_client_ip(request)

        api_logger.info(
            "REQUEST  %s %s | User: %s | IP: %s",
            method, path, user, ip
        )

        # ── Process request ────────────────────────────────────────
        response = self.get_response(request)

        # ── Capture response info ──────────────────────────────────
        duration_ms = (time.time() - start_time) * 1000
        status_code = response.status_code

        log_message = "RESPONSE %s %s | Status: %s | Time: %.2fms | User: %s"
        log_args = (method, path, status_code, duration_ms, user)

        if status_code >= 500:
            body = self._get_request_body(request)
            api_logger.error(
                log_message + " | Body: %s", *log_args, body
            )
        elif status_code >= 400:
            body = self._get_request_body(request)
            api_logger.warning(
                log_message + " | Body: %s", *log_args, body
            )
        else:
            api_logger.info(log_message, *log_args)

        return response

    # ── Helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _get_client_ip(request):
        """Extract client IP, respecting X-Forwarded-For."""
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')

    @staticmethod
    def _get_request_body(request):
        """Safely extract request body for error logging."""
        try:
            body = request.body.decode('utf-8')
            # Mask sensitive fields
            try:
                data = json.loads(body)
                for key in ('password', 'token', 'refresh', 'access', 'secret'):
                    if key in data:
                        data[key] = '***'
                return json.dumps(data)
            except (json.JSONDecodeError, TypeError):
                return body[:500]  # Truncate non-JSON bodies
        except Exception:
            return '<unable to read body>'
