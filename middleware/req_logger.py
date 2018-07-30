"""Request logger."""
import time
import logging
from flask import g
from flask import request

logger = logging.getLogger('file')
WARNING_TIME_OUT = 3000


class RequestLogger(object):
    """flask request logger."""

    def __init__(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def before_request(self):
        """Before request hook."""
        g.start_time = time.time()

    def after_request(self, response):
        """Response hook."""
        req_time = round((time.time() - g.start_time) * 1000)
        logger.info('API-{} request time is {} ms'.format(request, req_time))
        # if req_time > WARNING_TIME_OUT:
        #     logger.warning(
        #         'API request time out, the request is {}'
        #         .format(request))
        return response
