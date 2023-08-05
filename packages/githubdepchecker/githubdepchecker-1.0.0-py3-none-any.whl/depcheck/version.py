"""Version information."""

import platform

__version__ = '1.0.0'


def get_version():
    """Return package-name __version__ python python_version."""
    return (f'pypyr {__version__} '
            f'python {platform.python_version()}')