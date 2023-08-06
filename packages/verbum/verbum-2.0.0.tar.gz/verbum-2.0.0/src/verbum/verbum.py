"""Bump versions."""
import enum
import re
import sys


if sys.version_info[0:2] < (3, 10):  # pragma: no cover
    raise RuntimeError("Script runs only with python 3.10 or newer.")


class BumpType(enum.Enum):
    """Supported version bump types."""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    ALPHA = "alpha"
    BETA = "beta"
    RC = "rc"
    POST = "post"


class MainVersionNumber(enum.Enum):
    """Supported main version numbers."""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


VERVSION_RE = re.compile(
    r"""
        (?x)
        ^
        (?P<major>\d+)
        \.(?P<minor>\d+)
        \.(?P<patch>\d+)
        (?:a(?P<alpha>\d+)|b(?P<beta>\d+)|rc(?P<rc>\d+))?
        (?:\.post(?P<post>\d+))?
        $
    """
)


class BumpError(ValueError):
    """Error for invalid bump selection."""


class Version:  # pylint: disable=too-many-instance-attributes
    """Representation of version string with functionality to bump versions."""

    def __init__(self, version: str) -> None:
        """Parse the version string into a `Version` instance.

        :param version: The version string to parse
        :raises ValueError: On invalid version strings
        """
        version_parts = VERVSION_RE.match(version)
        if not version_parts:
            raise ValueError(f"Unparsable version: {version}")

        self._major = int(version_parts.group("major"))
        self._minor = int(version_parts.group("minor"))
        self._patch = int(version_parts.group("patch"))

        match version_parts.group("alpha"):
            case None:
                self._alpha = None
            case "0":
                raise ValueError("0 is not a valid alpha counter.")
            case _:
                self._alpha = int(version_parts.group("alpha"))

        match version_parts.group("beta"):
            case None:
                self._beta = None
            case "0":
                raise ValueError("0 is not a valid beta counter.")
            case _:
                self._beta = int(version_parts.group("beta"))

        match version_parts.group("rc"):
            case None:
                self._rc = None
            case "0":
                raise ValueError("0 is not a valid rc counter.")
            case _:
                self._rc = int(version_parts.group("rc"))

        match version_parts.group("post"):
            case None:
                self._post = None
            case "0":
                raise ValueError("0 is not a valid post counter.")
            case _:
                self._post = int(version_parts.group("post"))

    def __repr__(self) -> str:
        """Show the version's components."""
        pre = ""
        if self._alpha:
            pre = f"alpha{self._alpha}"
        if self._beta:
            pre = f"beta{self._beta}"
        if self._rc:
            pre = f"rc{self._rc}"

        return (
            "Version <"
            f"major={self._major} "
            f"minor={self._minor} "
            f"patch={self._patch} "
            f"pre={pre or False} "
            f"post={self._post or False}"
            ">"
        )

    def __str__(self) -> str:
        """Build a version string from the single components."""
        new_version = f"{self._major}.{self._minor}.{self._patch}"
        if self._alpha != 0 and self._alpha is not None:
            new_version += f"a{self._alpha}"
        if self._beta != 0 and self._beta is not None:
            new_version += f"b{self._beta}"
        if self._rc != 0 and self._rc is not None:
            new_version += f"rc{self._rc}"
        if self._post != 0 and self._post is not None:
            new_version += f".post{self._post}"

        return new_version

    def bump_major(self) -> None:
        """Bump the major version.

        What happens:

        - the major version is incremented by one
        - the minor and patch versions are reset to 0
        - all post- and pre-release segments are dropped
        """
        self._major += 1
        self._minor = self._patch = self._alpha = self._beta = self._rc = self._post = 0

    def bump_minor(self) -> None:
        """Bump the minor version.

        What happens:

        - the major version stays unchanged
        - the minor version is incremented by one
        - the patch version is reset to 0
        - all post- and pre-release segments are dropped
        """
        self._minor += 1
        self._patch = self._alpha = self._beta = self._rc = self._post = 0

    def bump_patch(self) -> None:
        """Bump the patch version.

        What happens:

        - the major and minor versions stay unchanged
        - the patch version is incremented by one
        - all post- and pre-release segments are dropped
        """
        self._patch += 1
        self._alpha = self._beta = self._rc = self._post = 0

    def bump_alpha(
        self, increase_if_not_alpha: MainVersionNumber = MainVersionNumber.PATCH
    ) -> None:
        """Bump the alpha version.

        What happens:

        If the version identifier already has an alpha segment:
        - increment the alpha version by one
        - drop post-release segment

        If the version identifier does not already have an alpha segment:
        - bump the specified main version by calling the respective ``bump_*`` method
        - set the alpha version to one
        - drop post-release segment

        :raises BumpError: if the version has a beta segment
        :raises BumpError: if the version has a release-candidate segment
        :param increase_if_not_alpha: Main version number to increment if not already an alpha
            version;
            defaults to ``MainVersionNumber.PATCH``
        """
        if self._beta != 0 and self._beta is not None:
            raise BumpError("Cannot bump 'alpha' version on a 'beta' release.")

        if self._rc != 0 and self._rc is not None:
            raise BumpError("Cannot bump 'alpha' version on a 'rc' release.")

        if self._alpha is not None:
            self._alpha += 1
            self._post = 0
            return

        match increase_if_not_alpha:
            case MainVersionNumber.MAJOR:
                self.bump_major()
            case MainVersionNumber.MINOR:
                self.bump_minor()
            case MainVersionNumber.PATCH:
                self.bump_patch()
        self._alpha = 1

    def bump_beta(self, increase_if_not_beta: MainVersionNumber = MainVersionNumber.PATCH) -> None:
        """Bum the beta version.

        What happens:

        If the version identifier already has a beta segment:
        - increment the beta version by one
        - drop post-release segment

        If the version identifier does not already have a beta segment:
        - bump the specified main version by calling the respective ``bump_*`` method
        - set the beta version to one
        - drop alpha- and post-release versions

        :raises BumpError: if the version has a release-candidate segment
        :param increase_if_not_beta: Main version number to increment if not already a beta version;
            defaults to ``MainVersionNumber.PATCH``
        """
        if self._rc != 0 and self._rc is not None:
            raise BumpError("Cannot bump 'beta' version on a 'rc' release.")

        if self._beta is not None:
            self._beta += 1
            self._post = 0
            return

        if self._alpha is not None:
            self._beta = 1
            self._alpha = self._post = 0
            return

        match increase_if_not_beta:
            case MainVersionNumber.MAJOR:
                self.bump_major()
            case MainVersionNumber.MINOR:
                self.bump_minor()
            case MainVersionNumber.PATCH:
                self.bump_patch()
        self._beta = 1

    def bump_rc(self, increase_if_not_rc: MainVersionNumber = MainVersionNumber.PATCH) -> None:
        """Bump the release-candidate version.

        What happens:

        If the version identifier already has a rc segment:
        - increment the rc version by one
        - drop post-release segment

        If the version identifier does not already have a rc segment:
        - bump the specified main version by calling the respective ``bump_*`` method
        - set the rc version to one
        - drop alpha-, beta- and post-release versions

        :param increase_if_not_rc: Main version number to increment if not already a rc version;
            defaults to ``MainVersionNumber.PATCH``
        """
        if self._rc is not None:
            self._rc += 1
            self._post = 0
            return

        if self._alpha is not None or self._beta is not None:
            self._rc = 1
            self._alpha = self._beta = self._post = 0
            return

        match increase_if_not_rc:
            case MainVersionNumber.MAJOR:
                self.bump_major()
            case MainVersionNumber.MINOR:
                self.bump_minor()
            case MainVersionNumber.PATCH:
                self.bump_patch()
        self._rc = 1

    def bump_post(self) -> None:
        """Bump the post version.

        What happens:

        If the version identifier already has a post-release segment:
        - increment the post-release version by one

        If the version identifier does not already have a post-release segment:
        - bump the specified main version by calling the respective ``bump_*`` method
        - set the rc version to one
        - drop alpha-, beta-, and post-release versions
        """
        self._post = (self._post or 0) + 1

    def make_final_release(self) -> None:
        """Drop pre-release segments.

        :raises BumpError: if the version is a final release with a post-release segment
        """
        if self._alpha is None and self._beta is None and self._rc is None:
            if self._post is not None:
                raise BumpError("Cannot make final release of a post-release from a final release.")
            raise BumpError("Cannot make final release of a final release.")

        self._alpha = self._beta = self._rc = self._post = 0

    def bump_version_by_type(self, increment_type: BumpType) -> None:
        """Bump the version by the specified type.

        :param increment_type: Version type to bump
        """
        match increment_type:
            case BumpType.MAJOR:
                self.bump_major()
            case BumpType.MINOR:
                self.bump_minor()
            case BumpType.PATCH:
                self.bump_patch()
            case BumpType.ALPHA:
                self.bump_alpha()
            case BumpType.BETA:
                self.bump_beta()
            case BumpType.RC:
                self.bump_rc()
            case BumpType.POST:
                self.bump_post()


def bump_version(version: str, increment_type: BumpType) -> str:
    """Bump a version string by a given type.

    :param version: Version string to bump
    :param increment_type: Version type to bump
    :return: Bumped version string
    """
    _version = Version(version)
    _version.bump_version_by_type(
        increment_type,
    )
    return str(_version)


def make_final_release(version: str) -> str:
    """Drop pre-release segments.

    :param version: Version string to bump
    :return: Bumped version string
    """
    _version = Version(version)
    _version.make_final_release()
    return str(_version)
