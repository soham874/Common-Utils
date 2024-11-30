from softeam_common_config.log_config import get_logger
import requests
from urllib.parse import urlencode, urljoin
import urllib.request

import PyPDF2

from opentelemetry.propagate import inject

log = get_logger(__name__)

session = requests.session()

default_headers = {
    "User-Agent": "insomnium/0.2.3-a"
}

def execute_rest_call(
        url,
        params = {},
        headers = {},
        payload = {},
        method = "GET"):
    
    inject(headers)
    merged_headers = {**default_headers, **headers}

    response = session.request(
        method=method,
        url=url,
        params=params,
        headers=merged_headers,
        data=payload
    )
            
    if not 200 <= response.status_code < 400:
        raise Exception (f"Failed to execute {method} call to URL {url} with status code {response.status_code} and response {response.text}")
    
    return response

def get_param_parsed_url(baseURL,queryParams):
    return urljoin(baseURL, '?' + urlencode(queryParams))

def download_file(file_url , save_name):
    urllib.request.urlretrieve(file_url , save_name)

def fetch_content_from_pdf(
    url,
    headers = {},
):
    merged_headers = {**default_headers, **headers}
    response = session.get(url, headers=merged_headers)

    pdf_path = 'download.pdf'
    with open(pdf_path, 'wb') as f:
        f.write(response.content)

    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        raw_content = ""
        for page in reader.pages:
            raw_content += page.extract_text()
    
    return raw_content