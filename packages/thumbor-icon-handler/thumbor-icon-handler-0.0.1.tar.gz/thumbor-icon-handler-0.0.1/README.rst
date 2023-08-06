thumbor-icon-handler
====================

A thumbor handler for serve favicon.icon request

Installation
------------

::

   pip install thumbor-icon-handler

Contribution
============

You can make a pull
requests[HERE]https://github.com/jjonline/thumbor-icon-handler/pulls,
thank you for your contribution.

# Configuration
===============

``HANDLER_LISTS`` settings
--------------------------

::

   HANDLER_LISTS = [
     'thumbor.handler_lists.healthcheck',
     'thumbor.handler_lists.upload',
     'thumbor.handler_lists.blacklist',
     # Add this config
     'thumbor_icon_handler.icon',
   ]

Optionally specify a local ``favicon.ico`` file
-----------------------------------------------

You can use the ``favicon.ico`` file in the local file system, or you
can ignore this configuration item and use the ``favicon.ico`` file in
the Loader

::

   # specify your local filesystem favicon.ico file full path
   # for example /srv/file/favicon.ico
   ICON_IMAGE_LOCAL_PATH = ''
