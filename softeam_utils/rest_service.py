from softeam_common_config.log_config import get_logger
import requests
from urllib.parse import urlencode, urljoin

log = get_logger(__name__)

def execute_rest_call(
        url,
        params = {},
        headers = {},
        payload = {},
        method = "GET"):
    
    default_headers = {
        "User-Agent": "insomnium/0.2.3-a"
    }

    response = requests.request(
        method = method,
        headers = default_headers | headers ,
        data = payload,
        params = params,
        url=url
    )
            
    if not 200 <= response.status_code < 400:
        raise Exception (f"Failed to execute {method} call to URL {url} with status code {response.status_code} and response {response.text}")
    
    return response

def get_param_parsed_url(baseURL,queryParams):
    return urljoin(baseURL, '?' + urlencode(queryParams))