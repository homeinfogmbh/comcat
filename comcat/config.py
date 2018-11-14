"""ComCat configuration."""

from configlib import INIParser


__all__ = ['CONFIG']


CONFIG = INIParser('/etc/comcat.conf', alert=True)
