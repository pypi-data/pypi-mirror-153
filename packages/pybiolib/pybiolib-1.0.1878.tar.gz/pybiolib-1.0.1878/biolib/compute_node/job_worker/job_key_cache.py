from biolib.compute_node.job_worker.cache_state import CacheState
from biolib.typing_utils import Dict

UuidStr = str
JobKeyCacheDict = Dict[UuidStr, str]


class JobKeyCacheState(CacheState[JobKeyCacheDict]):
    @property
    def _state_path(self) -> str:
        return f'{super()._cache_dir}/job-key-cache-state.json'

    def _get_default_state(self) -> JobKeyCacheDict:
        return {}
