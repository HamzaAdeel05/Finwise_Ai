from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
from langchain_community.cache import SQLiteCache

_current_cache = None

def configure_cache(cache_type):
    global _current_cache

    if cache_type == "SQLiteCache":
        _current_cache = SQLiteCache(database_path=".langchain_cache.db")
    else:
        _current_cache = InMemoryCache()

    set_llm_cache(_current_cache)
    return _current_cache
