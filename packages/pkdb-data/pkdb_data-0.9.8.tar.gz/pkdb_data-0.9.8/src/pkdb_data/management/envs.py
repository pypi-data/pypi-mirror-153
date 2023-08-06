"""Access to important environment variables."""
import os
from urllib.parse import urljoin

from pymetadata.log import get_logger


logger = get_logger(__name__)

try:
    API_BASE = os.environ["API_BASE"]
    # fix terminal slash
    if API_BASE.endswith("/"):
        API_BASE = API_BASE[:-1]

    USER = os.environ["USER"]
    PASSWORD = os.environ["PASSWORD"]
    DEFAULT_USER_PASSWORD = "pkdb"

    API_URL = urljoin(API_BASE, "api/v1")

except KeyError:
    logger.error(
        f"Environment variables have not been initialized. "
        f"1. add authentication credentials; and 2. run [blue]set -a && source .env.local[/]"
    )
    logger.error(f"")

    exit()
