#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-06-02
Purpose: Why not?
"""

from virustotal_tddschn.virustotal_sum_search import (
    create_arg_parser,
    parse_args,
    print_path_and_open_vt_link,
    brew_get_file_path,
    get_checksum_from_brew_file,
    get_brew_cache_path,
    sha256_checksum,
)
from . import __app_name__, __description__, __version__


def get_args():
    parser = create_arg_parser(
        __app_name__,
        __version__,
        __description__,
        add_help=False,
        brew_related_options_only=True,
    )
    parser.add_argument('-help', action='help', help='Show this help message and exit')
    args = parse_args(parser, brew_related_options_only=True)
    return args


def main():
    args = get_args()
    if brew_cache := args.brew_cache:
        file_path = get_brew_cache_path(brew_cache, use_cask=args.cask)
        hash = sha256_checksum(file_path)  # type: ignore
        print_path_and_open_vt_link(file_path, hash, args)
    else:
        brew_file_path = brew_get_file_path(brew_name=args.brew, use_cask=args.cask)
        if brew_file_path is None:
            print('No such formula or cask: {}'.format(args.brew))
            return
        hash = get_checksum_from_brew_file(brew_file_path=brew_file_path)
        file_path = brew_file_path
        print_path_and_open_vt_link(file_path, hash, args)


if __name__ == '__main__':
    main()
