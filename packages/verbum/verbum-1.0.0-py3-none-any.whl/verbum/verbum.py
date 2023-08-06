"""Bump versions."""
import enum
import re
import sys


if sys.version_info[0:2] < (3, 10):
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
    DEV = "dev"


VERVSION_RE = re.compile(
    r"""
        (?x)
        ^
        (?P<major>\d+)
        \.(?P<minor>\d+)
        \.(?P<patch>\d+)
        (?:a(?P<alpha>\d+)|b(?P<beta>\d+)|rc(?P<rc>\d+))?
        (?:\.post(?P<post>\d+))?
        (?:\.dev(?P<dev>\d+))?
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

        match version_parts.group("dev"):
            case None:
                self._dev = None
            case "0":
                raise ValueError("0 is not a valid dev counter.")
            case _:
                self._dev = int(version_parts.group("dev"))

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
            f"post={self._post or False} "
            f"dev={self._dev or False}"
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
        if self._dev != 0 and self._dev is not None:
            new_version += f".dev{self._dev}"

        return new_version

    def bump_major(self) -> None:
        """Bump the major version."""
        self._major += 1
        self._minor = self._patch = self._alpha = self._beta = self._rc = self._post = self._dev = 0

    def bump_minor(self) -> None:
        """Bump the minor version."""
        self._minor += 1
        self._patch = self._alpha = self._beta = self._rc = self._post = self._dev = 0

    def bump_patch(self) -> None:
        """Bump the patch version."""
        self._patch += 1
        self._alpha = self._beta = self._rc = self._post = self._dev = 0

    def bump_alpha(self) -> None:
        """Bum the alpha version.

        :raises BumpError: if the version has a beta identifier
        :raises BumpError: if the version has a release-candidate identifier
        """
        if self._beta != 0 and self._beta is not None:
            raise BumpError("Cannot bump 'alpha' version on a 'beta' release.")

        if self._rc != 0 and self._rc is not None:
            raise BumpError("Cannot bump 'alpha' version on a 'rc' release.")

        if self._alpha is None:
            self._alpha = 0
        self._alpha += 1

        if self._post != 0 and self._post is not None:
            self._patch += 1
            self._alpha = 1

        self._post = self._dev = 0

    def bump_beta(self) -> None:
        """Bum the beta version.

        :raises BumpError: if the version has a release-candidate identifier
        """
        if self._rc != 0 and self._rc is not None:
            raise BumpError("Cannot bump 'beta' version on a 'rc' release.")

        if self._beta is None:
            self._beta = 0
        self._beta += 1

        if self._post != 0 and self._post is not None:
            self._patch += 1
            self._beta = 1

        self._alpha = self._post = self._dev = 0

    def bump_rc(self) -> None:
        """Bump the release-candidate version."""
        if self._rc is None:
            self._rc = 0
        self._rc += 1

        if self._post != 0 and self._post is not None:
            self._patch += 1
            self._rc = 1

        self._alpha = self._beta = self._post = self._dev = 0

    def bump_post(self) -> None:
        """Bump the post version."""
        if self._post is None:
            self._post = 0
        self._post += 1
        self._dev = 0

    def bump_dev(self) -> None:
        """Bump the dev version."""
        if self._dev is None:
            self._dev = 0
        self._dev += 1

    def bump_version_by_type(self, increase_type: BumpType) -> None:
        """Bump the version by the specified type.

        :param increase_type: Version type to bump
        """
        match increase_type:
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
            case BumpType.DEV:
                self.bump_dev()


def bump_version(version: str, increase_type: BumpType) -> str:
    """Bump a version string by a given type.

    :param version: Version string to bump
    :param increase_type: Version type to bump
    :return: Bumped version string
    """
    _version = Version(version)
    _version.bump_version_by_type(increase_type)
    return str(_version)
