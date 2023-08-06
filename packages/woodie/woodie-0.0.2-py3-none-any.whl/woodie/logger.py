import logging


class Logger(logging.Logger):
    def __init__(self, name: str):
        self.fields = {}
        super().__init__(name)

    def _log(self, extra=None, **kwargs):
        fields = self.fields
        if isinstance(extra, dict):
            fields.update(extra)
        super()._log(**kwargs, extra=fields)
