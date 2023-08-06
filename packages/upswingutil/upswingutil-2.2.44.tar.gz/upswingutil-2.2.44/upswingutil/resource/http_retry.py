from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests


def http_retry():
    retry_strategy = Retry(
        total=3,
        status_forcelist=[400, 403, 429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "POST", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    return http
