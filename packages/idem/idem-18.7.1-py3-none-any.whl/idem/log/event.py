import logging.handlers


def wrapper(hub, **kwargs):
    class AsyncQueueWrapper:
        def __init__(self):
            self.profile = kwargs.get("profile", "idem-logger")

        def put_nowait(self, record: logging.LogRecord):
            hub.idem.event.put_nowait(
                profile=self.profile,
                body=record.getMessage(),
                tags={
                    "module": record.module,
                    "level": record.levelname.strip(),
                    "timestamp": str(record.asctime).strip(),
                },
            )

    return AsyncQueueWrapper()


def setup(hub, conf):
    """
    Log to the ingress queue
    """
    root = logging.getLogger()

    raw_level = conf["log_level"].strip().lower()
    if raw_level.isdigit():
        hub.log.INT_LEVEL = int(raw_level)
    else:
        hub.log.INT_LEVEL = hub.log.LEVEL.get(raw_level, root.level)

    root.setLevel(hub.log.INT_LEVEL)
    cf = logging.Formatter(fmt=conf["log_fmt_console"], datefmt=conf["log_datefmt"])
    ch = logging.StreamHandler()
    ch.setLevel(hub.log.INT_LEVEL)
    ch.setFormatter(cf)
    root.addHandler(ch)

    ff = logging.Formatter(fmt=conf["log_fmt_logfile"], datefmt=conf["log_datefmt"])
    _, kwargs = hub.render.cli.args(conf["log_handler_options"])

    qh = logging.handlers.QueueHandler(hub.log.queue.wrapper(**kwargs))
    qh.setLevel(hub.log.INT_LEVEL)
    qh.setFormatter(ff)
    root.addHandler(qh)
