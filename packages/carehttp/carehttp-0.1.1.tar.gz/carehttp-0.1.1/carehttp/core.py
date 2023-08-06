import requests
import check_suffix
from retrying import retry
from loguru import logger


def careget(url, mark=None, params=None, **kwargs):
    response = Carehttp(mark=mark).req('get', url, params=params, **kwargs)
    return response


def carepost(url, mark=None, data=None, json=None, **kwargs):
    response = Carehttp(mark=mark).req('post', url, data=data, json=json, **kwargs)
    return response


def _retry_if_err(exception, cls):
    """Return True if we should retry, False otherwise."""
    if cls.mark:
        obj = cls.mark
    else:
        obj = cls.url  # what object does it for

    logger.error(f'{obj} {cls.fetch_type.upper()} attempt{cls.attempt} ERR: {exception}')

    # Let's say we will just retry if any kind of exception occurred
    return isinstance(exception, Exception)


class Carehttp:
    def __init__(self, mark=None, tries=5, delay=1, max_delay=30):
        self.mark = mark  # Could be title, target name, but not url
        self.attempt = 0
        self.method = None
        self.url = None

        # retry setting
        self.tries = tries
        self.delay = delay * 1000
        self.max_delay = max_delay * 1000

        # Decorate functions to be retried
        retry_decorator = retry(
            stop_max_attempt_number=self.tries,  # retry times
            wait_exponential_multiplier=self.delay,
            wait_exponential_max=self.max_delay,
            retry_on_exception=lambda exc: _retry_if_err(exc, self),
        )

        self.req = retry_decorator(self.req)

    def req(self, method, url, **kwargs):
        self.url = url
        self.attempt += 1  # requests attempt times

        self._log_type(url, method)

        response = None
        try:
            response = requests.request(method, url, **kwargs)
            return response
        except Exception as e:
            raise e
        finally:
            response and response.close()

    def _log_type(self, url, method):
        """Change fetch type"""
        suffix_type = check_suffix.check_type(url)
        if suffix_type:
            self.fetch_type = suffix_type
        else:
            self.fetch_type = method


if __name__ == '__main__':
    r = careget('https://media.architecturaldigest.com/photos/62816958c46d4bf6875e71ff/master/pass/Gardening%20mistakes%20to%20avoid.jpg',
                mark='title',
                timeout=0.1,
                )
    print(r.text)
