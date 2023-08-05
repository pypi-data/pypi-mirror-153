# Imports to hide
from biolib import typing_utils as _typing_utils
from biolib.app import BioLibApp as _BioLibApp
from biolib.biolib_logging import logger as _logger, logger_no_user_data as _logger_no_user_data
from biolib.biolib_api_client import BiolibApiClient as _BioLibApiClient
from biolib.jobs import Job as _Job
from biolib import user as _user

import biolib.api
import biolib.app
import biolib.cli
import biolib.utils


# ------------------------------------ Function definitions for public Python API ------------------------------------

def call_cli() -> None:
    biolib.cli.main()


def load(uri: str) -> _BioLibApp:
    return _BioLibApp(uri)


def get_job(job_id: str) -> _Job:
    return _Job(uuid=job_id)


def sign_in() -> None:
    _user.sign_in()


def sign_out() -> None:
    _user.sign_out()


def login() -> None:
    sign_in()


def logout() -> None:
    sign_out()


def set_api_base_url(api_base_url: str) -> None:
    _BioLibApiClient.initialize(base_url=api_base_url)


def set_api_token(api_token: str) -> None:
    api_client = _BioLibApiClient.get()
    api_client.sign_in_with_api_token(api_token)


def set_log_level(level: _typing_utils.Union[str, int]) -> None:
    _logger.setLevel(level)
    _logger_no_user_data.setLevel(level)


# -------------------------------------------------- Configuration ---------------------------------------------------
__version__ = biolib.utils.BIOLIB_PACKAGE_VERSION
_DEFAULT_LOG_LEVEL = 'INFO' if biolib.utils.IS_RUNNING_IN_NOTEBOOK else 'WARNING'
_logger.configure(default_log_level=_DEFAULT_LOG_LEVEL)
_logger_no_user_data.configure(default_log_level=_DEFAULT_LOG_LEVEL)

set_api_base_url(biolib.utils.BIOLIB_BASE_URL)
