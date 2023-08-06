import os
import abc
import json
import time
from datetime import datetime

import appdirs  # type: ignore

from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger_no_user_data
from biolib.typing_utils import Optional, Generic, TypeVar

StateType = TypeVar('StateType')


class CacheStateError(BioLibError):
    pass


class CacheState(abc.ABC, Generic[StateType]):
    _cache_dir: str = appdirs.user_cache_dir(appname='pybiolib', appauthor='biolib')

    @property
    @abc.abstractmethod
    def _state_path(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_default_state(self) -> StateType:
        raise NotImplementedError

    @property
    def _state_lock_path(self) -> str:
        return f'{self._state_path}.lock'

    def __init__(self):
        self._state: Optional[StateType] = None

    def __enter__(self) -> StateType:
        logger_no_user_data.debug(f'CacheState: Entering state path: {self._state_path}...')
        self._acquire_state_lock()
        if os.path.exists(self._state_path):
            with open(self._state_path, mode='r') as file:
                self._state = json.loads(file.read())
        else:
            self._state = self._get_default_state()
            with open(self._state_path, mode='w') as file:
                file.write(json.dumps(self._state))

        # Check for type checking
        if self._state is None:
            raise CacheStateError('Internal state is not defined')

        return self._state

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        with open(self._state_path, mode='w') as file:
            file.write(json.dumps(self._state))

        self._release_state_lock()
        logger_no_user_data.debug(f'CacheState: Exited state path: {self._state_path}')

    def _acquire_state_lock(self) -> None:
        timeout_seconds = 5.0
        seconds_to_sleep = 0.5

        while os.path.exists(self._state_lock_path):
            time.sleep(seconds_to_sleep)
            timeout_seconds -= seconds_to_sleep
            if timeout_seconds < 0:
                raise CacheStateError('Cache state timed out waiting for lock file')

        os.makedirs(self._cache_dir, exist_ok=True)
        lock_file = open(self._state_lock_path, mode='x')
        lock_file.close()

    def _release_state_lock(self) -> None:
        if os.path.exists(self._state_lock_path):
            os.remove(self._state_lock_path)
        else:
            raise CacheStateError('Cache state was not locked.')

    @staticmethod
    def get_timestamp_now() -> str:
        return datetime.now().isoformat()
