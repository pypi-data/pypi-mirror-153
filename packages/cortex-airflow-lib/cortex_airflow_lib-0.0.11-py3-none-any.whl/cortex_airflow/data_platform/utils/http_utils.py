from http.client import responses
import re
import requests
import time
from requests.exceptions import RequestException

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import logging

def requests_retry_session(
    retries=5,
    backoff_factor=10,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_html_from_web_page(url: str) -> str:
    """Get html content from page by url

    Parameters
    ----------
    url : str
        url to the web page 
    
    Returns
    -------
    str
        a str with the html content  
    """
    try:
        with requests_retry_session().get(url) as r:
            if r.ok:
                html_page = r.text
                r.close()
                return html_page
            else:
                logging.info("status %s", r.status_code)
                logging.info("retry get_html_from_web_page()")
                time.sleep(10)
                get_html_from_web_page(url)
    except RequestException as e:
        logging.info("error %s", e)
        logging.info("retry get_html_from_web_page()")
        time.sleep(10)
        get_html_from_web_page(url)


def download_file_from_link(link, folder: str) -> str:    
    """Download file from url link and save on folder destiny

    Parameters
    ----------
    link : str
        Link of the file to be downloaded 
    folder : str
        Destination folder where the file will be saved
    """
    logging.info("download_file_from_link %s", link)
    try:
        with requests_retry_session().get(link, stream=True) as r:
            filename = ''
            if "Content-Disposition" in r.headers.keys():
                filename = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
            else:
                filename = link.split("/")[-1]

            with open(folder + '/' + filename, 'wb') as handle:
                for block in r.iter_content(1024):
                    handle.write(block)
                handle.close()
            r.close()
        logging.info("download complete %s", link)
        return filename
    except RequestException as e:
        logging.info("error %s", e)
        logging.info("retry download_file_from_link()")
        time.sleep(10)
        download_file_from_link(link, folder)


def post_with_retry(url, headers, data, files, json):
    response = {}

    try:
        response =  requests_retry_session().post(url, headers, data, files, json)
    except RequestException as e:
        logging.info("error %s", e)
        logging.info("retry post_with_retry()")
        post_with_retry(url, headers, data, files)

    return response