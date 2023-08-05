from typing import Text, List


class UnsupportedPackageManager(Exception):
    """
    raised when a cli package manager is not supported (eg: cnside [x] install ... <- "x" is not a supported package
    manager)
    """
    pass


class UnsupportedAction(Exception):
    """
    raised when a cli action is not supported (eg: cnside pip [x] <- "x" is not a supported action)
    """
    pass


class NotAuthenticated(Exception):
    """
    raised when the user is not authenticated.
    """
    pass


class FailedToLoadToken(Exception):
    """
    raised when authenticator fails to load token from disk.
    """
    pass


class FailedToRefreshToken(Exception):
    """
    raised when authenticator fails to refresh token.
    """
    pass


class ManifestNotFoundError(Exception):
    """
    raised when a manifest install is requested but no manifest file found.
    """
    pass


class LockfileNotFoundError(Exception):
    """
    raised when a lockfile is not found.
    """
    pass


class LockfileGenerateFailed(Exception):
    def __init__(self, command: List[Text], suggestion: List[Text], caution: Text, std_err: List[Text],
                 *args: object) -> None:
        super().__init__(*args)

        self.command = command
        self.suggestion = suggestion
        self.caution = caution
        self.std_err = std_err


class TerminateRequest(Exception):
    pass


class FailedPackageResolution(Exception):
    pass


class FailedSwitchYarnVersion(Exception):
    pass
