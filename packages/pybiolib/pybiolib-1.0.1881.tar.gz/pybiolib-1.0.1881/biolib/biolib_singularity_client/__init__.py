from spython.main import Client # type: ignore
from biolib.biolib_logging import logger


class BiolibSingularityClient:
    singularity_client = None

    @staticmethod
    def get_singularity_client():
        if BiolibSingularityClient.singularity_client is None:
            # version() returns empty string when singularity is not installed
            if Client.version() == '':
                raise Exception('Could not get singularity version')

            BiolibSingularityClient.singularity_client = Client
            logger.debug(f"Running Singularity: {BiolibSingularityClient.singularity_client.version()}")

        return BiolibSingularityClient.singularity_client

    @staticmethod
    def is_singularity_running():
        try:
            BiolibSingularityClient.get_singularity_client()
            return True
        except Exception:  # pylint: disable=broad-except
            return False
