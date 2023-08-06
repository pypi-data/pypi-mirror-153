"""Tests for verbum.verbum module."""
import pytest

from verbum import verbum


class TestParsing:
    """Test parsing of version string with ``Verson``."""

    @staticmethod
    @pytest.mark.parametrize(
        "version_str", ["1.1.1.1", "12.1.1.1", "1.12.1.1", "1.1.12.1", "1.1.1.12"]
    )
    def test_parsing_four_number_version(version_str: str) -> None:
        """Test 4 number versions are invalid."""
        with pytest.raises(ValueError, match=f"Unparsable version: {version_str}"):
            verbum.Version(version_str)

    @staticmethod
    @pytest.mark.parametrize("version_str", ["1.1.1", "12.1.1", "1.12.1", "1.1.12"])
    def test_parsing_three_number_version(version_str: str) -> None:
        """Test 3 number versions are valid."""
        verbum.Version(version_str)  # act

    @staticmethod
    @pytest.mark.parametrize("version_str", ["1.1", "12.1", "1.12"])
    def test_parsing_two_number_version(version_str: str) -> None:
        """Test 2 number versions are invalid."""
        with pytest.raises(ValueError, match=f"Unparsable version: {version_str}"):
            verbum.Version(version_str)

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [
            f"{v}{pre}"
            for v in ["1.1.1", "12.1.1", "1.12.1", "1.1.12"]
            for pre in [
                "-a1",
                ".a1",
                "_a1",
                "alpha1",
                "-b1",
                ".b1",
                "_b1",
                "beta1",
                "-rc1",
                ".rc1",
                "_rc1",
                "c1",
            ]
        ],
    )
    def test_parsing_invalid_pre_release(version_str: str) -> None:
        """Test invalid pre-releases."""
        with pytest.raises(ValueError, match=f"Unparsable version: {version_str}"):
            verbum.Version(version_str)

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [
            f"{v}{pre}"
            for v in ["1.1.1", "12.1.1", "1.12.1", "1.1.12"]
            for pre in ["a1", "b1", "rc1"]
        ],
    )
    def test_parsing_valid_pre_release(version_str: str) -> None:
        """Test valid pre-releases."""
        verbum.Version(version_str)  # act

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [
            f"{v}{pre}"
            for v in ["1.1.1", "12.1.1", "1.12.1", "1.1.12"]
            for pre in ["post1", "-post1", "_post1"]
        ],
    )
    def test_parsing_invalid_post_release(version_str: str) -> None:
        """Test invalid post-releases."""
        with pytest.raises(ValueError, match=f"Unparsable version: {version_str}"):
            verbum.Version(version_str)

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [f"{v}.post1" for v in ["1.1.1", "12.1.1", "1.12.1", "1.1.12"]],
    )
    def test_parsing_valid_post_release(version_str: str) -> None:
        """Test valid post-releases."""
        verbum.Version(version_str)  # act

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [
            f"{v}{pre}"
            for v in ["1.1.1", "12.1.1", "1.12.1", "1.1.12"]
            for pre in ["dev1", "-dev1", "_dev1"]
        ],
    )
    def test_parsing_invalid_dev_release(version_str: str) -> None:
        """Test invalid dev-releases."""
        with pytest.raises(ValueError, match=f"Unparsable version: {version_str}"):
            verbum.Version(version_str)

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [f"{v}.dev1" for v in ["1.1.1", "12.1.1", "1.12.1", "1.1.12"]],
    )
    def test_parsing_valid_dev_release(version_str: str) -> None:
        """Test valid dev-releases."""
        verbum.Version(version_str)  # act

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [
            f"{v}{pre}"
            for v in ["1.1.1", "12.1.1", "1.12.1", "1.1.12"]
            for pre in ["a0", "b0", "rc0", ".post0", ".dev0"]
        ],
    )
    def test_parsing_identifier_with_0(version_str: str) -> None:
        """Test identifier with 0 are invalid."""
        with pytest.raises(ValueError, match=r"0 is not a valid [a-z]{2,5} counter"):
            verbum.Version(version_str)


class TestReprAndStr:
    """Test __repr__ and __str__ methods of ``Verson``."""

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [
            "1.1.1",
            "12.1.1",
            "1.12.1",
            "1.1.12",
            "1.1.1a1",
            "1.1.1b1",
            "1.1.1rc1",
            "1.1.1.post1",
            "1.1.1.dev1",
            "1.1.1rc1.post1.dev1",
        ],
    )
    def test_str_is_equal_to_input(version_str: str) -> None:
        """Test __str__ is equal to the input string, if not bumped."""
        result = str(verbum.Version(version_str))

        assert result == version_str

    @staticmethod
    @pytest.mark.parametrize(
        ("version_str", "repr_str"),
        [
            ("1.1.1", "Version <major=1 minor=1 patch=1 pre=False post=False dev=False>"),
            ("1.1.1a1", "Version <major=1 minor=1 patch=1 pre=alpha1 post=False dev=False>"),
            ("1.1.1b1", "Version <major=1 minor=1 patch=1 pre=beta1 post=False dev=False>"),
            ("1.1.1rc1", "Version <major=1 minor=1 patch=1 pre=rc1 post=False dev=False>"),
            ("1.1.1.post1", "Version <major=1 minor=1 patch=1 pre=False post=1 dev=False>"),
            ("1.1.1.dev1", "Version <major=1 minor=1 patch=1 pre=False post=False dev=1>"),
            ("1.1.1rc1.post1.dev1", "Version <major=1 minor=1 patch=1 pre=rc1 post=1 dev=1>"),
        ],
    )
    def test_repr(version_str: str, repr_str: str) -> None:
        """Test __repr__."""
        result = repr(verbum.Version(version_str))

        assert result == repr_str


class TestBumping:
    """Test different bumping methods."""

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [
            "1.1.1",
            "1.1.1a1",
            "1.1.1b1",
            "1.1.1rc1",
            "1.1.1.post1",
            "1.1.1.dev1",
            "1.1.1rc1.post1.dev1",
        ],
    )
    def test_major_bump(version_str: str) -> None:
        """Test major version bump."""
        version = verbum.Version(version_str)

        version.bump_major()  # act

        assert str(version) == "2.0.0"

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [
            "1.1.1",
            "1.1.1a1",
            "1.1.1b1",
            "1.1.1rc1",
            "1.1.1.post1",
            "1.1.1.dev1",
            "1.1.1rc1.post1.dev1",
        ],
    )
    def test_minor_bump(version_str: str) -> None:
        """Test minor version bump."""
        version = verbum.Version(version_str)

        version.bump_minor()  # act

        assert str(version) == "1.2.0"

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        [
            "1.1.1",
            "1.1.1a1",
            "1.1.1b1",
            "1.1.1rc1",
            "1.1.1.post1",
            "1.1.1.dev1",
            "1.1.1rc1.post1.dev1",
        ],
    )
    def test_patch_bump(version_str: str) -> None:
        """Test patch version bump."""
        version = verbum.Version(version_str)

        version.bump_patch()  # act

        assert str(version) == "1.1.2"

    @staticmethod
    @pytest.mark.parametrize(
        ("version_str", "result_str"),
        [
            ("1.1.1", "1.1.1a1"),
            ("1.1.1a1", "1.1.1a2"),
            ("1.1.1.post1", "1.1.2a1"),
            ("1.1.1.dev1", "1.1.1a1"),
            ("1.1.1a1.post1.dev1", "1.1.2a1"),
        ],
    )
    def test_alpha_bump(version_str: str, result_str: str) -> None:
        """Test alpha version bump."""
        version = verbum.Version(version_str)

        version.bump_alpha()  # act

        assert str(version) == result_str

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        ["1.1.1b1", "1.1.1rc1", "1.1.1rc1.post1.dev1"],
    )
    def test_invalid_alpha_bump(version_str: str) -> None:
        """Test alpha version bump."""
        version = verbum.Version(version_str)

        with pytest.raises(
            verbum.BumpError, match=r"Cannot bump 'alpha' version on a '(beta|rc)' release"
        ):
            version.bump_alpha()

    @staticmethod
    @pytest.mark.parametrize(
        ("version_str", "result_str"),
        [
            ("1.1.1", "1.1.1b1"),
            ("1.1.1a1", "1.1.1b1"),
            ("1.1.1b1", "1.1.1b2"),
            ("1.1.1.post1", "1.1.2b1"),
            ("1.1.1.dev1", "1.1.1b1"),
            ("1.1.1a1.post1.dev1", "1.1.2b1"),
            ("1.1.1b1.post1.dev1", "1.1.2b1"),
        ],
    )
    def test_beta_bump(version_str: str, result_str: str) -> None:
        """Test beta version bump."""
        version = verbum.Version(version_str)

        version.bump_beta()  # act

        assert str(version) == result_str

    @staticmethod
    @pytest.mark.parametrize(
        "version_str",
        ["1.1.1rc1", "1.1.1rc1.post1.dev1"],
    )
    def test_invalid_beta_bump(version_str: str) -> None:
        """Test beta version bump."""
        version = verbum.Version(version_str)

        with pytest.raises(verbum.BumpError, match=r"Cannot bump 'beta' version on a 'rc' release"):
            version.bump_beta()

    @staticmethod
    @pytest.mark.parametrize(
        ("version_str", "result_str"),
        [
            ("1.1.1", "1.1.1rc1"),
            ("1.1.1a1", "1.1.1rc1"),
            ("1.1.1b1", "1.1.1rc1"),
            ("1.1.1rc1", "1.1.1rc2"),
            ("1.1.1.post1", "1.1.2rc1"),
            ("1.1.1.dev1", "1.1.1rc1"),
            ("1.1.1a1.post1.dev1", "1.1.2rc1"),
            ("1.1.1b1.post1.dev1", "1.1.2rc1"),
            ("1.1.1rc1.post1.dev1", "1.1.2rc1"),
        ],
    )
    def test_rc_bump(version_str: str, result_str: str) -> None:
        """Test rc version bump."""
        version = verbum.Version(version_str)

        version.bump_rc()  # act

        assert str(version) == result_str

    @staticmethod
    @pytest.mark.parametrize(
        ("bump_type", "result_str"),
        [
            (verbum.BumpType.MAJOR, "2.0.0"),
            (verbum.BumpType.MINOR, "1.2.0"),
            (verbum.BumpType.PATCH, "1.1.2"),
            (verbum.BumpType.ALPHA, "1.1.1a1"),
            (verbum.BumpType.BETA, "1.1.1b1"),
            (verbum.BumpType.RC, "1.1.1rc1"),
            (verbum.BumpType.POST, "1.1.1.post1"),
            (verbum.BumpType.DEV, "1.1.1.dev1"),
        ],
    )
    def test_bump_by_type(bump_type: verbum.BumpType, result_str: str) -> None:
        """Test ``bump_version_by_type`` method."""
        version = verbum.Version("1.1.1")

        version.bump_version_by_type(bump_type)  # act

        assert str(version) == result_str


@pytest.mark.parametrize(
    ("bump_type", "result_str"),
    [
        (verbum.BumpType.MAJOR, "2.0.0"),
        (verbum.BumpType.MINOR, "1.2.0"),
        (verbum.BumpType.PATCH, "1.1.2"),
        (verbum.BumpType.ALPHA, "1.1.1a1"),
        (verbum.BumpType.BETA, "1.1.1b1"),
        (verbum.BumpType.RC, "1.1.1rc1"),
        (verbum.BumpType.POST, "1.1.1.post1"),
        (verbum.BumpType.DEV, "1.1.1.dev1"),
    ],
)
def test_version_bump_function(bump_type: verbum.BumpType, result_str: str) -> None:
    """Test ``bump_version`` function."""
    result = verbum.bump_version("1.1.1", bump_type)

    assert result == result_str
