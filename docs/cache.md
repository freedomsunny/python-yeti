# python
目前支持同步及异步redis

## 使用方法
### sync
```python
from yeti.cache.cache import CacheFactory
sync_cache_obj = CacheFactory()

# storage
sync_cache_obj.cache.set(key, value)

# get
sync_cache_obj.cache.get(key)
```

### async
```python
from yeti.cache.cache import aio_redis
async_cache_obj = aio_redis()

# storage
await async_cache_obj.set(key, value)

# get
await async_cache_obj.get(key)

```