"""
Definition of command line commands after installing pkdb_data package.

Upload study or studies, delete studies and upload available info nodes.

"""
import argparse
from pathlib import Path

from pymetadata.log import get_logger

import pkdb_data.management.api as api
from pkdb_data.management.envs import API_BASE, API_URL, PASSWORD, USER
from pkdb_data.management.index import update_study_index
from pkdb_data.management.manage import InfoUploader, create_info_nodes
from pkdb_data.management.query import check_json_response, get_authentication_headers
from pkdb_data.management.upload_studies import UploadClient


logger = get_logger(__name__)


def create_info_nodes_command():
    """Create info_nodes JSON."""
    parser = argparse.ArgumentParser(description="Create info_nodes for PKDB")

    parser.set_defaults(func=create_info_nodes)
    args = parser.parse_args()
    args.func(args)


def upload_info_nodes_command():
    """Upload info_nodes to PKDB."""
    parser = argparse.ArgumentParser(description="Upload info_nodes to PKDB")
    parser.add_argument(
        "--url",
        "-u",
        help="url to PKDB backend",
        dest="url_base",
        type=str,
        required=False,
    )
    parser.set_defaults(func=upload_info_nodes)
    args = parser.parse_args()
    args.func(args)


def upload_studies_command():
    """Upload single study in PKDB."""
    parser = argparse.ArgumentParser(description="Upload studies to PKDB")
    parser.add_argument(
        "--substances",
        "-s",
        help="relative path(s) to studies directories",
        dest="substances",
        type=str,
        required=False,
        nargs="+",
    )

    parser.add_argument(
        "--ignore_studies",
        "-i",
        help="relative path(s) to studies directories which will be ignored during upload.",
        dest="ignore_studies",
        type=str,
        required=False,
        nargs="+",
    )
    parser.add_argument(
        "--url",
        "-u",
        help="url to PKDB backend",
        dest="url_base",
        type=str,
        required=False,
    )
    parser.set_defaults(func=upload_studies)
    args = parser.parse_args()
    args.func(args)


def upload_study_command():
    """Upload single study in PKDB."""
    parser = argparse.ArgumentParser(description="Upload study to PKDB")
    parser.add_argument(
        "--study",
        "-s",
        help="path to study directory",
        dest="study",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--url",
        "-u",
        help="url to PKDB backend",
        dest="url_base",
        type=str,
        required=False,
    )
    parser.set_defaults(func=upload_study)
    args = parser.parse_args()
    args.func(args)


def delete_study_command():
    """Delete single study in PKDB."""
    parser = argparse.ArgumentParser(description="Delete study in PKDB")
    parser.add_argument(
        "--sid",
        "-s",
        help="study identifier (sid)",
        dest="study_sid",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--url", "-u", help="url to PKDB backend", dest="url_base", type=str
    )
    parser.set_defaults(func=delete_study)
    args = parser.parse_args()
    args.func(args)


def upload_info_nodes(args):
    """Upload InfoNodes JSONs."""
    api_url, auth_headers = _pkdb_api_info(args)
    InfoUploader.setup_database(api_url=api_url, auth_headers=auth_headers)


def upload_studies(args):
    """Upload studies to

    :return:
    """
    substances = getattr(args, "substances", None)
    ignore_studies = getattr(args, "ignore_studies", None)

    if not substances:
        substances = [
            "acetaminophen",
            "atorvastatin",
            "bicarbonate",
            "caffeine",
            "cholesterol",
            "codeine",
            "dextromethorphan",
            "diazepam",
            "glucose",
            "ibuprofen",
            "icg",
            "methacetin",
            "metoprolol",
            "midazolam",
            "morphine",
            "omeprazole",
            "oxazepam",
            "pravastatin",
            "simvastatin",
            "sparteine",
            "torasemide",
        ]
    api_url, auth_headers = _pkdb_api_info(args)
    up_client = UploadClient(api_url=api_url, auth_headers=auth_headers, client=None)
    up_client.upload_studies_for_substances(
        relative_paths=substances, ignore_studies=ignore_studies
    )


def upload_study(args):
    """Upload a single study to PKDB."""
    api_url, auth_headers = _pkdb_api_info(args)
    up_client = UploadClient(api_url=api_url, auth_headers=auth_headers, client=None)
    up_client.upload_study(study_dir_path=Path(args.study))


def delete_study(args):
    """Delete a single study in PKDB."""
    study_sid = args.study_sid
    logger.info(f"delete: {study_sid}")

    api_url, auth_headers = _pkdb_api_info(args)
    up_client = UploadClient(api_url=api_url, auth_headers=auth_headers, client=None)
    response = up_client.delete_instance(api.STUDIES, study_sid)
    check_json_response(response)

    # non-thread/non-process indexing
    update_study_index(study_sid, api_url, auth_headers)


def _pkdb_api_info(args):
    """Get connection information."""
    url_base = getattr(args, "url_base")
    if url_base:
        if url_base.endswith("/"):
            url_base = url_base[:-1]
        api_url = f"{url_base}/api/v1"
    else:
        url_base = API_BASE
        api_url = API_URL

    auth_headers = get_authentication_headers(
        url_base, username=USER, password=PASSWORD
    )
    return api_url, auth_headers
