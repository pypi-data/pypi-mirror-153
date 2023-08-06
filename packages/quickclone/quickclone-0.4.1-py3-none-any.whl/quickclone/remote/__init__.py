from __future__ import annotations
import typing as t

from .locators import *
from .scp import *


SCM_WITH_EXPLICIT_SCP: t.Set[str] = {"git"}
"""
A set of version control systems that I currently know that support SCP
locators.
"""


def remote_to_string(remote: UniformResourceLocator, scm: str) -> str:
    """
    Convert a locator to string form.
    
    Parameters
    ----------
    remote: UniformResourceLocator
        The locator identifying the remote repository.
    
    scm: str
        The version control system used to manage the remote repository.
    
    Returns
    -------
    str
        The locator in string form.
    """
    if (
        remote.get_scheme() == "ssh" and
        remote.kwargs.get("explicit_scp") and
        scm in SCM_WITH_EXPLICIT_SCP
    ):
        scp_locator = ScpLocator.from_locator(remote)
        if remote.get_username() == "": # Separate if statements for other SCMs.
            if scm == "git":
                scp_locator.username = "git"
        return str(scp_locator)
    else:
        return str(remote)
