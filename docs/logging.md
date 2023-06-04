# 日志
## 日志级别

|级别|值|对应方法|
| :-----| ----: | :----: |
|TRACE|5|logger.trace()|
|DEBUG|10|logger.debug()|
|INFO|20|logger.info()|
|SUCCESS|25|logger.success()|
|WARNING|30|logger.warning()|
|ERROR|40|logger.error()|
|CRITICAL|50|logger.critical()|
## 使用日志
```python
from yeti.log.logger import LOG
LOG.info("your context")
```