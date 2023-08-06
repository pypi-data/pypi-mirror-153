"""Templates for Nox extension."""

from functools import partial

from pyscaffold.templates import ScaffoldOpts, get_template

template = partial(get_template, relative_to=__name__)


def init(opts: ScaffoldOpts) -> str:
    """Template __init__.py.

    :param opts: mapping parameters dictionary
    :returns: file content as string
    """
    if opts["package"] == opts["name"]:
        opts["distribution"] = "__name__"
    else:
        opts["distribution"] = '"{0}"'.format(opts["name"])
    template_src = template("__init__.py")
    return template_src.substitute(opts)
