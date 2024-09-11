from django.core.cache import cache
from django.db.models.manager import BaseManager
from typing import Any, Callable

from django.utils.encoding import force_bytes
import hashlib


class BaseCachingMixin:
    cache_timeout = 60 * 15  

    def _cache_key(self, key: str) -> str:
        """Generate a cache key."""
        key = hashlib.md5(force_bytes(key)).hexdigest()
        return f"cache_{key}"

    def get_cached_data(self, key: str, data_callable: Callable, *args, **kwargs) -> Any:
        """Retrieve data from cache or compute it if not cached."""
        cache_key = self._cache_key(key)
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = data_callable(*args, **kwargs)
            cache.set(cache_key, cached_data, self.cache_timeout)
        return cached_data
    
    def get_cached_query(self, key: str, query: BaseManager[Any]):
        cache_key = self._cache_key(key)
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = list(query)
            cache.set(cache_key, cached_data, self.cache_timeout)
        return cached_data