# -*- coding: utf-8 -*-
import datetime

from thumbor.handlers import ContextHandler
from thumbor.utils import logger
from os.path import exists


def renderIconFromLocal(path):
    """ get favicon.ico from specify full-path af first"""
    with open(path, "rb") as source_file:
        return source_file.read()


class IconHandler(ContextHandler):
    async def get(self):
        local_path = self.context.config.get("ICON_IMAGE_LOCAL_PATH")
        loader_path = 'favicon.ico'

        if local_path is not None and local_path.strip() != '' and exists(local_path):
            res = renderIconFromLocal(local_path)
        else:
            res = await self.renderIconFromLoader(loader_path)

        if res is not None:
            self.set_status(200)
            self.set_header("Content-Type", 'image/x-icon')

            max_age = self.context.config.MAX_AGE
            if max_age:
                self.set_header(
                    "Cache-Control", "max-age=" + str(max_age) + ",public"
                )
                self.set_header(
                    "Expires",
                    datetime.datetime.utcnow()
                    + datetime.timedelta(seconds=max_age),
                )
            self.write(res)
            await self.finish()
        else:
            self._error(404, "favicon.ico do not found in storage")

    async def renderIconFromLoader(self, path):
        """ get favicon.ico from Loader """
        loader_res = await self.context.modules.loader.load(self.context, path)
        if loader_res is not None:
            logger.debug("[icon-handler] loader found favicon.ico")
            return loader_res.buffer
        else:
            logger.debug("[icon-handler] loader do not found favicon.ico")
            return None
