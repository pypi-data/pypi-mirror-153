import logging
import os
import time


RESOURCES_ROOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "resources")
)
logging.info(f'RESOURCES_ROOT_PATH = "{RESOURCES_ROOT_PATH}"')


def get_resource_path(sub_path):
    return os.path.join(
        RESOURCES_ROOT_PATH, sub_path.replace("{ts}", time.strftime("(%y%m%d.%H%M%S)"))
    )
