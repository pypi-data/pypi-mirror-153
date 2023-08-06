import time
from functools import wraps

from requests import HTTPError

from kikyo_utils.constants import RETRY_API_TIMES

RETRY_HTTP_CODES = {500, 502, 503, 504, 522, 524, 408, 429}


class NotRetry(Exception):
    @property
    def error(self) -> str:
        return self.args[0]


def retry_rest_api(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        last_error = None

        if 'retry' in kwargs:
            retry: int = kwargs.pop('retry')
        else:
            retry = RETRY_API_TIMES
        if 'retry_wait' in kwargs:
            retry_wait: int = kwargs.pop('retry_wait')
        else:
            retry_wait = 3

        k = retry
        while k >= 0:
            try:
                return func(*args, **kwargs)
            except NotRetry as e:
                last_error = e.error
                k = 0
            except HTTPError as e:
                last_error = e
                if e.response is not None and e.response.status_code not in RETRY_HTTP_CODES:
                    k = 0
            k -= 1
            if k >= 0 and retry_wait > 0:
                time.sleep(retry_wait)
        if last_error is not None:
            raise last_error

    return wrapped
