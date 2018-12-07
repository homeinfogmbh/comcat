"""ComCat configuration."""

from configlib import INIParser


__all__ = ['CONFIG']


CONFIG = INIParser('/usr/local/etc/comcat.conf', alert=True)
