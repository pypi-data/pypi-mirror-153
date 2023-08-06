"""
All functions manipulating the elastic index.
"""
import multiprocessing
import threading
import time
from datetime import timedelta

import requests
from pymetadata.log import get_logger

from pkdb_data.management.query import check_json_response, requests_with_client


logger = get_logger(__name__)


class IndexProcess(multiprocessing.Process):
    """Process for indexing elastic."""

    def __init__(self, sid, api_url, auth_headers, client=None):
        multiprocessing.Process.__init__(
            self,
            target=_update_study_index_log,
            args=(sid, api_url, auth_headers, client),
        )


class IndexThread(threading.Thread):
    """Thread for indexing elastic."""

    def __init__(self, sid, api_url, auth_headers, client=None):
        threading.Thread.__init__(self)
        self.sid = sid
        self.api_url = api_url
        self.auth_headers = auth_headers
        self.client = client

    def run(self):
        _update_study_index_log(self.sid, self.api_url, self.auth_headers, self.client)


def _update_study_index_log(sid, api_url, auth_headers, client=None):
    logger.info(f"Start indexing {sid}")
    start_time = time.time()
    update_study_index(
        sid=sid, api_url=api_url, auth_headers=auth_headers, client=client
    )
    index_time = timedelta(seconds=time.time() - start_time).total_seconds()
    logger.info(f"[white on black]Finished indexing {sid} in {index_time:.2f} [s]")


def update_study_index(sid, api_url, auth_headers, client=None):
    """Updates the elasticsearch index for given study_sid."""
    response = requests_with_client(
        client,
        requests,
        f"{api_url}/update_index/",
        method="post",
        data={"sid": sid},
        headers=auth_headers,
    )
    check_json_response(response)
