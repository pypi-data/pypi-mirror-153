"""
Python RPC Client for Discord
-----------------------------
By: qwertyquerty and LewdNeko
"""

from .baseclient import BaseClient
from .client import Client, AioClient
from .exceptions import *
from .presence import Presence, AioPresence


__title__ = 'discordrpc'
__author__ = 'UlifSystems'
__copyright__ = 'Copyright 2022 UlifSystems'
__license__ = 'MIT'
__version__ = '4.2.1'