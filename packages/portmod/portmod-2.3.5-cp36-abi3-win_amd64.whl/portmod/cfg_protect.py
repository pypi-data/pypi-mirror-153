# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import csv
import filecmp
import os
import shutil
from difflib import unified_diff
from logging import info
from pathlib import Path
from string import Template
from tempfile import NamedTemporaryFile
from typing import Generator, Iterable, List, Optional, Tuple

from portmodlib.execute import execute
from portmodlib.fs import match
from portmodlib.l10n import l10n
from portmodlib.parsers.list import add_list, read_list

from .config import get_config_value, variable_data_dir
from .globals import env
from .prompt import prompt_options


def get_protected_path(file: str) -> str:
    new_file = file
    i = 1
    while os.path.exists(new_file):
        name, ext = os.path.splitext(new_file)
        if ext.startswith(".__cfg_protect"):
            new_file = name + f".__cfg_protect_{i}__"
            i += 1
        else:
            new_file = file + ".__cfg_protect__"
    return new_file


def is_protected(file: str) -> bool:
    protected = get_config_value("CFG_PROTECT")
    if isinstance(protected, list):
        for pattern in protected:
            if match(Path(file).absolute().relative_to(env.prefix().ROOT), pattern):
                return True
    elif isinstance(protected, str):
        if match(Path(file).absolute().relative_to(env.prefix().ROOT), protected):
            return True
    return False


def get_mergetool() -> Optional[str]:
    """Returns user-configured mergetool"""
    result = get_config_value("MERGE_TOOL")
    if result:
        return str(result)
    return None


def merge_files(source: str, dest: str):
    """Invokes user-configured mergetool"""
    mergetool = get_mergetool()
    assert mergetool
    execute(
        Template(mergetool).substitute(
            orig=f'"{source}"', new=f'"{dest}"', merged=f'"{dest}"'
        )
    )


def get_redirections() -> Generator[Tuple[str, str], None, None]:
    """
    Iterates over all previously made file redirections and returns the (non-empty)
    results
    """
    if os.path.exists(os.path.join(env.prefix().CONFIG_PROTECT_DIR, "cfg_protect.csv")):
        with open(
            os.path.join(env.prefix().CONFIG_PROTECT_DIR, "cfg_protect.csv"), "r"
        ) as file:
            reader = csv.reader(file)
            for row in reader:
                dst = row[0]
                src = row[1]

                if os.path.exists(src) and os.stat(src).st_size != 0:
                    yield src, dst


def remove_redirection(src: str, dst: str):
    path = os.path.join(env.prefix().CONFIG_PROTECT_DIR, "cfg_protect.csv")
    if os.path.exists(path):
        with open(path, "w") as output_file:
            writer = csv.writer(output_file)
            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    row_dst = row[0]
                    row_src = row[1]
                    if row_dst != dst and row_src != src:
                        writer.writerow(row)


def get_changes(src: str, dst: str) -> List[str]:
    if os.path.islink(src):
        src_lines = [l10n("symlink-to", path=os.readlink(src)) + "\n"]
    else:
        try:
            with open(src, "r") as src_file:
                src_lines = src_file.readlines()
        except UnicodeDecodeError:
            src_lines = ["<" + l10n("binary-data") + ">\n"]
    dst_lines = []
    if os.path.lexists(dst):
        if os.path.islink(dst):
            dst_lines = [l10n("symlink-to", path=os.readlink(dst)) + "\n"]
        else:
            try:
                with open(dst, "r") as dst_file:
                    dst_lines = dst_file.readlines()
            except UnicodeDecodeError:
                dst_lines = ["<" + l10n("binary-data") + ">\n"]

    return list(unified_diff(dst_lines, src_lines, dst, src))


def handle_cfg_protect(files: Iterable[Tuple[str, str]]):
    """Prompts user to allow changes to files made by modules"""
    whitelist_file = os.path.join(variable_data_dir(), "module-data", "file-whitelist")
    blacklist_file = os.path.join(variable_data_dir(), "module-data", "file-blacklist")
    blacklist = set()
    whitelist = set()
    if os.path.exists(whitelist_file):
        whitelist = set(read_list(whitelist_file))
    if os.path.exists(blacklist_file):
        blacklist = set(read_list(blacklist_file))

    # Display file changes to user and prompt
    for src, dst in files:
        original_src = src
        if os.path.exists(dst) and filecmp.cmp(src, dst, shallow=False):
            os.remove(src)
            continue

        if dst in blacklist:
            info(l10n("skipped-blacklisted-file", file=dst))
            os.remove(src)
            continue

        while True:
            output = get_changes(src, dst)
            if dst in whitelist:
                # User won't be prompted, so we should still display output, but supress it
                # unless running verbosely
                info("".join(output))
            else:
                print("".join(output))

            print()

            if dst not in whitelist and not env.INTERACTIVE:
                info(l10n("skipped-update-noninteractive", file=dst))
                break

            response = None
            if dst not in whitelist:
                options = [
                    (l10n("yes-short"), l10n("apply-change")),
                    (l10n("always-short"), l10n("merge-apply-always")),
                    (l10n("skip-change.short"), l10n("skip-change")),
                    (l10n("no-short"), l10n("merge-do-not-apply-change")),
                    (l10n("never-short"), l10n("merge-apply-never")),
                ]
                mergetool = get_mergetool()
                if mergetool:
                    options.append(
                        (
                            l10n("mergetool.short"),
                            l10n("mergetool", mergetool=f'"{mergetool}"'),
                        )
                    )
                else:
                    print(l10n("mergetool-info", var="MERGE_TOOL"))

                try:
                    response = prompt_options(l10n("apply-above-change-qn"), options)
                except EOFError:
                    response = l10n("no.short")

            if response == l10n("skip-change.short"):
                break

            if dst in whitelist or response in (
                l10n("yes-short"),
                l10n("always-short"),
            ):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(dst) or os.path.islink(dst):
                    os.remove(dst)
                shutil.move(src, dst)
                # Remove the original file if src now points to a merged file
                if original_src != src:
                    os.remove(original_src)

                if response == l10n("always-short"):
                    add_list(whitelist_file, dst)

                remove_redirection(src, dst)
                break

            if response == l10n("mergetool.short"):
                with open(dst, "r") as file:
                    contents = file.read()
                with NamedTemporaryFile(
                    "w",
                    delete=False,
                    prefix="EDITME.",
                    suffix="." + os.path.basename(dst),
                ) as tempfile:
                    tempfile.write(contents)
                    tempfile_path = tempfile.name
                # Merge against intermediate file
                merge_files(src, tempfile_path)
                # Don't break, as we must let the user accept the merged changes first
                src = tempfile_path

            if response in {l10n("no-short"), l10n("never-short")}:
                if response == l10n("never-short"):
                    add_list(blacklist_file, dst)

                os.remove(src)
                remove_redirection(src, dst)
                break
