# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import csv
import os

from .globals import config_protect_dir


def _add_redirection(source: str, dest: str):
    protect_dir = os.path.join(config_protect_dir())
    csv_path = os.path.join(protect_dir, "cfg_protect.csv")
    if os.path.exists(csv_path):
        with open(csv_path, "r") as file:
            reader = csv.reader(file)

            if [dest, source] not in reader:
                with open(csv_path, "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([dest, source])
    else:
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([dest, source])


def create_file(path):
    """
    Returns the path to be used for redirection
    and adds it to the list of redirected paths
    """
    protect_dir = os.path.join(config_protect_dir())
    new_path = os.path.join(protect_dir, os.path.basename(path) + ".cfg_protect")
    if os.path.lexists(new_path):
        num = 1
        new_path = new_path + "." + str(num)

        while os.path.lexists(new_path):
            num += 1
            new_path, _ = os.path.splitext(new_path)
            new_path = new_path + "." + str(num)

    os.makedirs(protect_dir, exist_ok=True)
    _add_redirection(new_path, path)

    return new_path
