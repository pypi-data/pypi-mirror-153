# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tests', 'verbum']

package_data = \
{'': ['*']}

modules = \
['AUTHORS']
extras_require = \
{'testing': ['pytest>=6.0',
             'pytest-cov>=3.0',
             'coverage[toml]>=6.0',
             'pytest-randomly>=3.0']}

setup_kwargs = {
    'name': 'verbum',
    'version': '1.0.0',
    'description': 'Python version bumper.',
    'long_description': '# verbum\n\nA version bumping library.\n\n## Examle\n\n```python\nfrom verbum import verbum\n\ncurrent_release = "1.1.1"\nnew_release = verbum.bump_version(current_release, verbum.BumpType.ALPHA)\nprint(new_release)  # 1.1.1a1\n```\n\n## Version strings\n\n### Input\n\nverbum is opinionated and version strings accepted by `bump_version` are a subset of valid strings\nspecified in [PEP440](https://peps.python.org/pep-0440/).\n\n### Output\n\nVersion strings output by `bump_version` are [PEP440](https://peps.python.org/pep-0440/) compliant.\n\n### Ruleset\n\n1. Three version numbers are mandatory: `X.Y.Z`.\n2. A leading forth number (epoch) is forbidden.\n3. Pre-release identifier like alpha, beta and release-candidates are only allowed with their\n   abbreviations:\n   - `alpha` -> `a`\n   - `beata` -> `b`\n   - `release-candidate` -> `rc`\n4. Other variante as `rc` are not supported for release-candidates.\n5. Pre-release identifier must follow the scheme `{a|b|rc}N` where `N` is an interger.\n6. Pre-release identifier must come behind the third version number.\n7. Post-release identifier must follow the scheme `.postN` where `N` is an interger.\n8. Post-release identifier must come behind the third version number or an optional pre-release\n   identifier.\n9. Dev-release identifier must follow the scheme `.devN` where `N` is an interger.\n10. Dev-release identifier must come last.\n11. Pre-release, post-release and dev-release counter must start with 1 not 0.\n    A 0 is interpreted as not set. This means e.g. bumping a post-release on this `1.1.1rc0`\n    would result in `1.1.1.post1`.\n12. Addition identifiers or separators are forbidden.\n\n### Examples\n\n```text\n1.2.3a1\n1.2.3b1\n1.2.3rc1\n1.2.3\n\n1.2.3.post1\n1.2.3a1.post1\n1.2.3b1.post1\n1.2.3rc1.post1\n\n1.2.3.dev1\n1.2.3a1.dev1\n1.2.3b1.dev1\n1.2.3rc1.dev1\n1.2.3.post1.dev1\n\n1.2.3rc1.post1.dev1\n```\n',
    'author': 'Christian Riedel',
    'author_email': 'cielquan@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cielquan/verbum',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
