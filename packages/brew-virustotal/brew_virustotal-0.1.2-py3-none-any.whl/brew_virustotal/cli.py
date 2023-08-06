#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-06-02
Purpose: Why not?
"""

from virustotal_tddschn.virustotal_sum_search import (
    get_args,
    print_path_and_open_vt_link,
    brew_get_file_path,
    get_checksum_from_brew_file,
    get_brew_cache_path,
    sha256_checksum,
)
from . import __app_name__, __description__, __version__


def main():
    args = get_args(
        __app_name__, __version__, __description__, brew_related_options_only=True
    )
    if brew_cache := args.brew_cache:
        file_path = get_brew_cache_path(brew_cache, use_cask=args.cask)
        hash = sha256_checksum(file_path)  # type: ignore
        print_path_and_open_vt_link(file_path, hash, args)
    else:
        brew_file_path = brew_get_file_path(brew_name=args.brew, use_cask=args.cask)
        hash = get_checksum_from_brew_file(brew_file_path=brew_file_path)
        file_path = brew_file_path
        print_path_and_open_vt_link(file_path, hash, args)


if __name__ == '__main__':
    main()
