# Copyright 2022 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from portmod.merge import global_updates
from portmodlib.l10n import l10n


def add_cfg_update_parser(subparsers, parents):
    parser = subparsers.add_parser(
        "cfg-update",
        help=l10n("cfg-update-help"),
        parents=parents,
        conflict_handler="resolve",
    )

    parser.set_defaults(func=lambda args: global_updates())
