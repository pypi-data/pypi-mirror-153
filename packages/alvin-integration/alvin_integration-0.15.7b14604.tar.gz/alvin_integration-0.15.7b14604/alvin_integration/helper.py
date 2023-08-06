import logging


class AlvinLoggerAdapter(logging.LoggerAdapter):
    """
    This allows for more flexible troubleshooting on Cloud platforms e.g. GCP Composer.
    Each log statement coming from this Alvin plugin has a [alvin] prefix.
    https://docs.python.org/3/howto/logging-cookbook.html#using-loggeradapters-to-impart-contextual-information
    """

    def process(self, msg, kwargs):
        return f"[alvin] {msg}", kwargs
