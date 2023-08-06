import typing as t

from quickclone.config.configurator import SmartConfigurator
from quickclone.local import local_dest_path
from quickclone.remote import UniformResourceLocator, remote_to_string

from .errors import InvalidVcsError
from .vcs.common import Command
from .vcs.git import GitCloneCommand
from .vcs.mercurial import MercurialCloneCommand


def create_clone_command(
    vcs: str,
    configs: SmartConfigurator,
    built_url: t.Union[UniformResourceLocator, str],
    dest_path: str = "",
    cla_list: t.Optional[t.Iterable[str]] = None,
    cla_dict: t.Optional[t.Mapping[str, str]] = None,
    ignored: t.Optional[t.Set[str]] = None
) -> Command:
    """
    Create a clone command for a version control system.
    
    Parameters
    ----------
    vcs: str
        Which version control system to use.
    
    configs: SmartConfigurator
        Configuration object.
    
    built_url: UniformResourceLocator | str
        The locator of the remote repository.
    
    dest_path: str = ""
        The local destination path of the cloned repository. The value of this
        argument should come from the command line instead of being the
        post-processed result from other functions.
    
    cla_list: Iterable[str] | None = None
        Extra command line arguments stored as an iterable.
    
    cla_dict: Dict[str, str] | None = None
        Extra command line arguments sotred as a mapping object.
    
    ignored: Set[str] | None = None
        Set of config options to ignore.
    
    Raises
    ------
    InvalidVcsError
        If `vcs` is invalid or not supported.
    
    Returns
    -------
    Command
        The command used to clone the remote repository.
    """
    if cla_list is None:
        cla_list = list()
    if cla_dict is None:
        cla_dict = dict()
    if ignored is None:
        ignored = set()
    
    built_url.detect_explicitness(
        configs.from_dotted_string("options.remote.force_scp"),
        "options.remote.force_scp" in ignored
    )
    final_url = remote_to_string(built_url, vcs)
    dest_path = local_dest_path(
        dest_path,
        configs.from_dotted_string("options.local.remotes_dir"),
        built_url.get_host(),
        built_url.get_path(),
        "options.local.remotes_dir" in ignored
    )
    
    return create_clone_command_with_processed(
        vcs,
        configs,
        final_url,
        dest_path,
        cla_list,
        cla_dict,
        ignored
    )


def create_clone_command_with_processed(
    vcs: str,
    configs: SmartConfigurator,
    final_url: str,
    dest_path: str,
    cla_list: t.Iterable[str],
    cla_dict: t.Mapping[str, str],
    ignored: t.Set[str]
) -> Command:
    """
    Create a clone command with the valid processed values passed in.
    """
    if vcs in {"git"}:
        return GitCloneCommand(final_url, dest_path, *cla_list, **cla_dict)
    elif vcs in {"mercurial", "hg"}:
        return MercurialCloneCommand(final_url, dest_path, *cla_list, **cla_dict)
    else:
        raise InvalidVcsError(vcs)
