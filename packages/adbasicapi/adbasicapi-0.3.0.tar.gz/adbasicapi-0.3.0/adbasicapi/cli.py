# -*- coding: utf-8 -*-

"""Console script for adbasicapi."""
import argparse
import sys

from adbasicapi.api import modify_record_targetIP, modify_record_cname


def changeIP():
    """Console script for adbasicapi."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str)
    parser.add_argument("-i", "--targetIP", type=str)
    parser.add_argument("-d", "--dry-run", action="store_true")

    kwargs = vars(parser.parse_args())
    ok = modify_record_targetIP(**kwargs)
    if ok:
        return 0
    return 1


def changeCNAME():
    """Console script for adbasicapi."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str)
    parser.add_argument("-c", "--cname_target", type=str)
    parser.add_argument("-d", "--dry-run", action="store_true")
    kwargs = vars(parser.parse_args())

    ok = modify_record_cname(**kwargs)
    if ok:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
