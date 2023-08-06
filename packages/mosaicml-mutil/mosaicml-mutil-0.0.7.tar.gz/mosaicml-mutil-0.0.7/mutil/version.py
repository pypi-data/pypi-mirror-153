""" M-Util Versioning """
__version_major__ = 0
__version_minor__ = 0
__version_patch__ = 7
__version_extras__ = ''
__version__ = f'v{__version_major__}.{__version_minor__}.{__version_patch__}{__version_extras__}'

current_version = None

try:
    from mcli.utils.utils_pypi import Version

    current_version = Version(
        major=__version_major__,
        minor=__version_minor__,
        patch=__version_patch__,
        extras=__version_extras__,
    )
except:
    pass


def print_version(**kwargs) -> int:
    del kwargs
    print(__version__)
    return 0
