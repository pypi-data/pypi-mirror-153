#!/usr/bin/env python

from .commands import core


def main():
    args = core.main_parser.parse_args()
    if hasattr(args, "handler"):
        core.setup()
        args.handler(args)
        return
    core.main_parser.print_help()


# if __name__ == "__main__":
#     from commands import core
#     core.main()
