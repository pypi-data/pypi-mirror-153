"""
Application config
"""

# Django
from django.apps import AppConfig

from . import __version__


class TnntDiscordbotCogsConfig(AppConfig):
    name = "tnnt_discordbot_cogs"
    label = "tnnt_discordbot_cogs"
    verbose_name = f"TN-NT Discordbot Cogs v{__version__}"
