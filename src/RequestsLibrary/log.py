import logging

from base64 import b64encode

from RequestsLibrary.utils import is_file_descriptor
from robot.api import logger


LOG_CHAR_LIMIT = 10000


def log_response(response, log_options=None):
    log_options = log_options or {}
    response_body_binary = log_options.get('response_body_binary', False)

    logger.info("%s Response : url=%s \n " % (response.request.method.upper(),
                                              response.url) +
                "status=%s, reason=%s \n " % (response.status_code,
                                              response.reason) +
                "body(base64=%s)=%s \n " % (
                    response_body_binary,
                    format_data_to_log_string(
                        response.content if response_body_binary else response.text,
                        encode=b64encode if response_body_binary else None
                    ))
                )


def log_request(response, log_options=None):
    log_options = log_options or {}
    request_body_binary = log_options.get('request_body_binary', False)

    request = response.request
    if response.history:
        original_request = response.history[0].request
        redirected = '(redirected) '
    else:
        original_request = request
        redirected = ''
    logger.info("%s Request : " % original_request.method.upper() +
                "url=%s %s\n " % (original_request.url, redirected) +
                "path_url=%s \n " % original_request.path_url +
                "headers=%s \n " % original_request.headers +
                "body(base64=%s)=%s \n " % (
                    request_body_binary,
                    format_data_to_log_string(
                        original_request.body,
                        encode=b64encode if request_body_binary else None
                    ))
                )


def format_data_to_log_string(data, limit=LOG_CHAR_LIMIT, encode=None):

    if not data:
        return None

    if is_file_descriptor(data):
        return repr(data)

    if len(data) > limit and logging.getLogger().level > 10:
        data = "%s... (set the log level to DEBUG or TRACE to see the full content)" % data[:limit]

    return encode(data).decode() if encode else data
