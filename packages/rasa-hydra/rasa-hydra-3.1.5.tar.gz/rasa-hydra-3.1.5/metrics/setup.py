import os
import logging

logger = logging.getLogger("Prometheus")


def set_prometheus_multiproc_dir(service):
    import uuid

    path = "/tmp/{}/{}".format(service, uuid.uuid4())
    os.makedirs(path)
    os.environ['prometheus_multiproc_dir'] = path
    logger.info("Prometheus multiproc dir has been set to {}.".format(path))