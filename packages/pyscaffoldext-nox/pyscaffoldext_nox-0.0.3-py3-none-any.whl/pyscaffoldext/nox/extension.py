"""Nox for pyscaffold."""
from functools import reduce
from typing import List

from configupdater import ConfigUpdater
from pyscaffold.actions import Action, ActionParams, ScaffoldOpts, Structure
from pyscaffold.extensions import Extension
from pyscaffold.operations import no_overwrite
from pyscaffold.structure import merge, reify_leaf, reject

from pyscaffoldext.nox.templates import template


class Nox(Extension):
    """
    This class serves as the skeleton for your new PyScaffold Extension. Refer
    to the official documentation to discover how to implement a PyScaffold
    extension - https://pyscaffold.org/en/latest/extensions.html
    """

    def activate(self, actions: List[Action]) -> List[Action]:
        """Activate extension. See :obj:`pyscaffold.extension.Extension.activate`."""
        actions = self.register(actions, add_files)
        return self.register(actions, replace_files, before="verify_project_dir")


def add_files(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Add extension files.

    See :obj:`pyscaffold.actions.Action`
    :param opts: scaffold options
    :param struct: structure
    :returns: action params
    """
    file_list = [
        "noxfile.py",
    ]

    files: Structure = {}

    for file_path in file_list:
        *dirs, file_name = file_path.split("/")

        files_descender = files
        for dir_ in dirs:
            files_descender = files_descender.setdefault(dir_, {})
        files_descender[file_name] = (template(file_name.strip(".")), no_overwrite())

    return merge(struct, files), opts


def configure_setup_cfg(content: str, opts: ScaffoldOpts) -> str:
    """Set customizations to setup.cfg.

    :param content: The content of the setup.cfg
    :param opts: scaffold options
    :returns: the modified content of the setup.cfg
    """
    updater = ConfigUpdater()
    updater.read_string(content)
    updater["options.extras_require"]["testing"].append("nox")
    return str(updater)


def replace_files(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Replace existing files.

    See :obj:`pyscaffold.actions.Action`
    :param opts: scaffold options
    :param struct: structure
    :returns: action params
    """
    # do setup.cfg modifications
    setup_content, setup_file_op = reify_leaf(struct["setup.cfg"], opts)
    struct["setup.cfg"] = (configure_setup_cfg(setup_content, opts), setup_file_op)

    # remove files for replacement
    replacement_files = [
        "tox.ini",
    ]

    struct = reduce(reject, replacement_files, struct)

    return struct, opts
