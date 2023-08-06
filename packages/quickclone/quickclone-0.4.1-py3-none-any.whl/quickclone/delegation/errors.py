class CommandNotFoundError(Exception):
    """
    Error for when a command could not be found in the current environment.
    """
    
    def __init__(self, command: str) -> None:
        self.command = command
    
    def __str__(self) -> str:
        return f"'{self.command}' could not be found."


class InvalidVcsError(Exception):
    """
    This error is raised when an invalid version control system is used.
    """
    
    def __init__(self, vcs: str) -> None:
        self.vcs = vcs
    
    def __str__(self) -> str:
        return (
            f"'{self.vcs}' is not a valid version control system or "
            "is not supported by QuickClone yet."
        )
