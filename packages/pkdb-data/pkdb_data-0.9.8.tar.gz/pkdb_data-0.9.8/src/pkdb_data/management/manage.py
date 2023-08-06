"""
Create all choices.
Stores JSON files for database upload.
"""
import collections
import json
import time
from datetime import timedelta
from pathlib import Path

import requests
from pymetadata.log import get_logger

from pkdb_data.management import api
from pkdb_data.management.envs import DEFAULT_USER_PASSWORD
from pkdb_data.management.query import (
    check_json_response,
    requests_with_client,
    sid_exists,
)
from pkdb_data.management.upload_studies import _log_step
from pkdb_data.management.users import USER_GROUPS_DATA, USERS_DATA
from pkdb_data.management.utils import read_json


logger = get_logger(__name__)

# directory for serialization
JSON_PATH = Path(__file__).parent.parent.parent / "json"


class InfoUploader(object):
    """Posting created choices JSONs to database."""

    @classmethod
    def setup_database(
        cls, api_url, auth_headers, client=None, json_path: Path = JSON_PATH
    ):
        """Creates core information in database by uploading the information
        from JSON files.

        :return:
        """
        logger.info(f"upload info nodes: [blue]{api_url}[/]")

        json_paths = {
            key: json_path / f"{key[1:]}.json"
            for key in [
                api.USER_GROUPS,
                api.USERS,
                api.INFO_NODES,
            ]
        }
        success = True

        for api_path, path in json_paths.items():
            data_json = read_json(path)

            # inject default password
            if api_path == "_users":
                for k, item in enumerate(data_json):
                    item["password"] = DEFAULT_USER_PASSWORD
                    data_json[k] = item

            if api_path in ["_users", "_user_groups"]:
                success = cls._upload_info(
                    api_url, api_path, auth_headers, data_json, client
                )

            if api_path in ["_info_nodes"]:
                cls.check_for_duplicates(data_json, path)
                success = cls._upload_info(
                    api_url, api_path, auth_headers, data_json, client
                )
        if success:
            logger.info(f"[green bold]SUCCESSFULLY UPLOADED INFO NODES[/]")

    @staticmethod
    def check_for_duplicates(data_json, path):
        a = [v["sid"] for v in data_json]
        for item, count in collections.Counter(a).items():
            if count > 1:
                logger.warning(
                    f"The JSON file <{path}> has duplicate entries. "
                    f"The instance with sid = {item} exists {count} times."
                )

    @staticmethod
    def _upload_info(api_url, choice, auth_headers, data_json, client=None):
        """Upload single choice.

        :param api_url:
        :param choice:
        :param auth_headers:
        :param data_json:
        :param client:
        :return:
        """
        start_time = time.time()
        if choice == "_info_nodes":
            response = requests_with_client(
                client,
                requests,
                f"{api_url}/{choice}/",
                method="post",
                data=data_json,
                headers=auth_headers,
            )

            success = check_json_response(response)
            if not success:
                logger.error(f"{choice} upload failed")
                return False
            upload_time = time.time() - start_time
            upload_time = timedelta(seconds=upload_time).total_seconds()
            _log_step(f"Upload {choice[1:]}", time=upload_time)
            return success

        success = True
        for instance in data_json:
            response = requests_with_client(
                client,
                requests,
                f"{api_url}/{choice}/",
                method="post",
                data=instance,
                headers=auth_headers,
            )
            if choice == "_info_nodes":
                if sid_exists(response):
                    response = requests_with_client(
                        client,
                        requests,
                        f"{api_url}/{choice}/{instance['sid']}/",
                        method="patch",
                        data=instance,
                        headers=auth_headers,
                    )
                success = check_json_response(response)

            if not success:
                logger.error(f"{choice} upload failed: {instance} ")
                return False

        upload_time = time.time() - start_time
        upload_time = timedelta(seconds=upload_time).total_seconds()
        _log_step(f"Upload {choice[1:]}", time=upload_time)
        return success


def create_info_nodes(args):
    """Creates all JSON files for info nodes upload."""
    logger.info(f"[blue]collect info nodes[/]")
    from pkdb_data.info_nodes.nodes import (  # local import to avoid warnings
        collect_nodes,
    )

    logger.info(f"[blue]create info nodes[/]")
    info_nodes = collect_nodes()
    info = {
        "info_nodes": [node.serialize(info_nodes) for node in info_nodes],
        "user_groups": USER_GROUPS_DATA,
        "users": USERS_DATA,
    }

    for key, data in info.items():
        with open(JSON_PATH / f"{key}.json", "w") as fp:
            json.dump(data, fp, indent=2)

    logger.info(f"[green bold]SUCCESSFULLY CREATED INFO_NODES JSON[/]")
