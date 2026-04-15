# Logging and Exceptions

`camouchat-core` provides dedicated infrastructure for strict typing on errors and custom formatting for centralized logging across all plugin ecosystems.

## Exceptions

The base element for error tracking is `CamouChatError`. All internal and plugin exceptions must inherit from this to ensure consistent traceback aggregation.

```python
from camouchat_core import CamouChatError

class PluginError(CamouChatError):
    pass
```

## Logging Factory

To ensure all plugins (such as `camouchat-browser` and `camouchat-whatsapp`) dump telemetry using unified layouts, use the `LoggerFactory` generating a `LoggerAdapter` configured for CLI UI outputs.

```python
from camouchat_core import LoggerFactory

logger = LoggerFactory.get_logger(name="MyPlugin")
logger.info("Plugin engaged.")
```
