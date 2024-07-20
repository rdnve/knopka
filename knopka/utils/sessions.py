import logging
import typing as ty

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

logger = logging.getLogger(__name__)

DEFAULT_RETRY_TOTAL: int = 0
DEFAULT_RETRY_BACKOFF_FACTOR: int = 1800
DEFAULT_RETRY_ALLOWED_METHODS: ty.Sequence[str] = ("POST", "GET")
DEFAULT_REQUEST_TIMEOUT: int = 2


def get_session(
    retry_total: int = DEFAULT_RETRY_TOTAL,
    retry_backoff_factor: int = DEFAULT_RETRY_BACKOFF_FACTOR,
    retry_allowed_methods: ty.Sequence[str] = DEFAULT_RETRY_ALLOWED_METHODS,
    headers: ty.Optional[ty.Mapping] = None,
    proxy_url: ty.Optional[str] = None,
) -> Session:
    """Custom session object w/ some settings"""

    session: Session = Session()

    if headers is not None:
        session.headers.update(headers)

    if proxy_url is not None:
        session.proxies = {"https": proxy_url, "http": proxy_url}

    if retry_total is not None:
        retries: Retry = Retry(
            total=retry_total,
            backoff_factor=retry_backoff_factor / 1000,
            allowed_methods=list(retry_allowed_methods),
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

    return session
