import argparse
import sys

from mcli import config

from mutil.util import get_util

MUTIL_USAGE = """Usage
> mutil <platform>
"""


def configure_parser(parser: argparse.ArgumentParser):
    conf = config.MCLIConfig.load_config()
    registered_platforms = conf.platforms
    registered_platform_names = [x.name for x in registered_platforms] + ['all']
    parser.add_argument(
        'platform',
        choices=registered_platform_names,
        default=registered_platform_names[0],
        help='What platform would you like to get util for?',
    )


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    configure_parser(parser)
    return parser


class NotInternal(Exception):
    """ Raised if not running as an internal user """


_NOT_INTERNAL_MESSSAGE = "You must be running as an internal user to use mutil"


def main() -> int:

    parser = get_parser()
    args = parser.parse_args()

    try:
        conf = config.MCLIConfig.load_config()
        if not conf.internal:
            raise NotInternal(_NOT_INTERNAL_MESSSAGE)
    except Exception:
        raise NotInternal(_NOT_INTERNAL_MESSSAGE)

    if len(vars(args)) == 0:
        parser.print_usage()
        return 1

    return get_util(platform=args.platform)


if __name__ == "__main__":
    sys.exit(main())
