# -*- coding: utf-8 -*-
""""
author: team tvb-sz
time  : 2022/6/6
file  : icon.py
"""

from typing import Any

from thumbor.handler_lists import HandlerList

from thumbor_icon_handler.handler import IconHandler
from thumbor.utils import logger


def get_handlers(context: Any) -> HandlerList:
    """ define /favicon.ico request handler
        if you use config `ICON_IMAGE_LOCAL_PATH` specify local filesystem favicon.ico full-path and that file is exist
        use local filesystem file response /favicon.ico request
        if you do not specify `ICON_IMAGE_LOCAL_PATH` config or that file do not exist,
        will use loader to try get favicon.ico
    """
    logger.debug("[icon-handler] init /favicon.icon handler")
    return [("/favicon.ico", IconHandler, {"context": context})]
