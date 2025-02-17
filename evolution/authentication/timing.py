import logging
import time

logger = logging.getLogger(__name__)

class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()
        response = self.get_response(request)
        duration = time.perf_counter() - start_time

        logger.debug(f"Request took {duration:.2f} seconds to process.")

        return response
