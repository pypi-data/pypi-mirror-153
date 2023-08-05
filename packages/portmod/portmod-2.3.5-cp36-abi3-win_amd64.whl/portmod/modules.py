# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Interface for interacting with installed modules
"""

import glob
import os
import shutil
from logging import info
from types import SimpleNamespace
from typing import Generator, List

from portmodlib.l10n import l10n

from .cfg_protect import get_redirections, handle_cfg_protect
from .config import get_config_value, variable_data_dir
from .globals import env
from .loader import load_module


class ModuleState(SimpleNamespace):
    TEMP: str
    ROOT: str
    CACHE: str


def do_func(state, func, args=None):
    if args is None:
        func(state)
    else:
        func(state, args)


class ModuleFunction:
    """Function defined by a module"""

    name: str

    def __init__(
        self, name: str, desc: str, do, options, parameters, state: ModuleState
    ):
        self.name = name
        self.desc = desc
        self.__do__ = do
        self.state = state
        if options is not None:
            self.options = options
        else:
            self.options = []
        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = []

    def do(self, args):
        """Execute action"""
        do_func(
            self.state,
            self.__do__,
            {key: getattr(args, key) for key in self.options},
        )

    def do_noargs(self):
        """Execute action without arguments"""
        do_func(self.state, self.__do__)

    def describe(self) -> str:
        """Returns string describing function"""
        return str(self.__do__.__doc__)


class Module:
    """Base module object"""

    def __init__(self, name: str, desc: str, funcs: List[ModuleFunction], state):
        self.funcs = {func.name: func for func in funcs}
        self.name = name
        self.desc = desc
        self.state = state
        os.makedirs(state.TEMP, exist_ok=True)
        os.makedirs(state.CACHE, exist_ok=True)

    def update(self):
        if "update" in self.funcs:
            self.funcs["update"].do_noargs()

    def add_parser(self, parsers, parents):
        parser = parsers.add_parser(self.name, help=self.desc, parents=parents)
        this_subparsers = parser.add_subparsers()
        for func in self.funcs.values():
            if func.name == "update":
                continue
            func_parser = this_subparsers.add_parser(func.name, help=func.desc)
            for option, parameter in zip(func.options, func.parameters):
                func_parser.add_argument(option, help=parameter)
            func_parser.set_defaults(func=func.do)

        def help_func(args):
            parser.print_help()

        parser.set_defaults(func=help_func)
        self.arg_parser = parser

        return self.arg_parser

    def prerm(self):
        if "prerm" in self.funcs:
            self.funcs["prerm"].do_noargs()

    def cleanup(self):
        shutil.rmtree(self.state.TEMP)


def get_state(module_name: str) -> ModuleState:
    return ModuleState(
        TEMP=os.path.join(env.TMP_DIR, "modules", module_name),
        ROOT=os.path.join(env.prefix().ROOT),
        CACHE=os.path.join(env.prefix().CACHE_DIR, "modules", module_name),
    )


def iterate_modules() -> Generator[Module, None, None]:
    """Returns a generator which produces all modules"""
    modules_dir = get_config_value("MODULEPATH")
    if modules_dir:
        modules_path = os.path.join(env.prefix().ROOT, modules_dir)
        for module_file in glob.glob(os.path.join(modules_path, "*.pmodule")):
            module_name, _ = os.path.splitext(os.path.basename(module_file))
            module = load_module(module_file, get_state(module_name))
            yield module
            module.cleanup()


def module_prerm(path: str):
    module_name, _ = os.path.splitext(os.path.basename(path))
    module = load_module(path, get_state(module_name))
    module.prerm()
    module.cleanup()


def update_modules():
    """Runs update function (if present) on all installed modules"""
    for module in iterate_modules():
        info(l10n("updating-module", name=module.name))
        module.update()

    handle_cfg_protect(get_redirections())


def add_parsers(parsers, parents) -> List[Module]:
    """Adds parsers for the modules to the given argument parser"""
    modules = []
    for module in iterate_modules():
        module.add_parser(parsers, parents)
        modules.append(module)
    return modules


def require_module_updates():
    """
    Creates a file that indicates that modules need to be updated
    """
    open(os.path.join(variable_data_dir(), ".modules_need_updating"), "a").close()


def clear_module_updates():
    """Clears the file indicating that modules need updating"""
    path = os.path.join(variable_data_dir(), ".modules_need_updating")
    if os.path.exists(path):
        os.remove(path)


def modules_need_updating():
    """Returns true if changes have been made since the config was sorted"""
    return os.path.exists(os.path.join(variable_data_dir(), ".modules_need_updating"))
