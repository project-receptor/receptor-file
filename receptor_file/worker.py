import json
import logging
import time
import uuid
from functools import partial
import receptor

logger = logging.getLogger(__name__)


def configure_logger():
    receptor_logger = logging.getLogger("receptor")
    logger.setLevel(receptor_logger.level)
    for handler in receptor_logger.handlers:
        logger.addHandler(handler)


@receptor.plugin_export(payload_type=receptor.BUFFER_PAYLOAD)
def execute(message, config, result_queue):
    configure_logger()
    filenm = f"/tmp/{uuid.uuid4()}.data"
    with open(filenm, "wb") as fd:
        written = 0
        for chunk in iter(partial(message.read, 4096), b""):
            fd.write(chunk)
            written += len(chunk)
            result_queue.put(f"Wrote {written} of {len(message)}")
    result_queue.put(f"Finished writing {filenm}")
