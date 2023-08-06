# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtcli', 'dtcli.scripts']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4,<6.0',
 'asn1crypto>=1.4,<2.0',
 'click-aliases>=1.0,<2.0',
 'click>=7.1,<8.0',
 'cryptography>=3.4,<4.0',
 'requests>=2.26,<3.0',
 'wheel>=0.36,<0.37']

entry_points = \
{'console_scripts': ['dt = dtcli.scripts.dt:main']}

setup_kwargs = {
    'name': 'dt-cli',
    'version': '1.1.0a1',
    'description': 'Dynatrace CLI',
    'long_description': '# dt-cli — Dynatrace developer\'s toolbox\n\nDynatrace CLI is a command line utility that assists in signing, building and uploading\nextensions for Dynatrace Extension Framework 2.0.\n\n<p>\n  <a href="https://pypi.org/project/dt-cli/"><img alt="PyPI" src="https://img.shields.io/pypi/v/dt-cli?color=blue&logo=python&logoColor=white"></a>\n  <a href="https://pypi.org/project/dt-cli/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/dt-cli?logo=python&logoColor=white"></a>\n  <a href="https://github.com/dynatrace-oss/dt-cli/actions/workflows/built-test-release.yml"><img alt="GitHub Workflow Status (main branch)" src="https://img.shields.io/github/workflow/status/dynatrace-oss/dt-cli/Build%20Test%20Release/main?logo=github"></a>\n</p>\n\n\n### Features\n\n* Build and sign extensions from source\n* Generate development certificates for extension signing\n* Generate CA certificates for development\n* Validate and upload extension to Dynatrace Extension Framework 2.0.\n\n## Installation\n\n```shell\npip install dt-cli\n```\n\n## Usage\n\n1. Generate certificates\n```sh\n  dt extension gencerts\n```\n2. Upload your `ca.pem` certificate to the Dynatrace credential vault\n\nSee: [Add your root certificate to the Dynatrace credential vault](https://www.dynatrace.com/support/help/extend-dynatrace/extensions20/sign-extension/#add-your-root-certificate-to-the-dynatrace-credential-vault)\n\n3. Build and sign, then upload extension\n```sh\n  dt extension build\n  dt extension upload\n```\nUse `dt extension --help` to learn more\n\n4. Download extension schemas\n```sh\n  dt extension schemas\n```\n_API permissions needed: `extensions.read`_\n\nThis script should only be needed once, whenever schema files are missing or you want to target a different version than what you already have. It does the following:\n* Downloads all the extension schema files of a specific version\n* Schemas are downloaded to `schemas` folder\n\n5. Wipes out extension from Dynatrace Cluster\n```sh\n  dt extension delete\n```\nUse `dt extension --help` to learn more\n\n\n## Using dt-cli from your Python code\n\nYou may want to use some commands implemented by `dt-cli` directly in your Python code, e.g. to automatically sign your extension in a CI environment.\nHere\'s an example of building an extension programatically, it assumes `dtcli` package is already installed and available in your working environment.\n\n\n```python\nfrom dtcli import building\n\n\nbuilding.build_extension(\n    extension_dir_path = \'./extension\',\n    extension_zip_path = \'./extension.zip\',\n    extension_zip_sig_path = \'./extension.zip.sig\',\n    target_dir_path = \'./dist\',\n    certificate_file_path = \'./developer.crt\',\n    private_key_file_path = \'./developer.key\',\n    dev_passphrase=None,\n    keep_intermediate_files=False,\n)\n```\n\n## Development\n\nSee our [CONTRIBUTING](CONTRIBUTING.md) guidelines and instructions.\n\n## Contributions\n\nYou are welcome to contribute using Pull Requests to the respective\nrepository. Before contributing, please read our\n[Code of Conduct](https://github.com/dynatrace-oss/dt-cli/blob/main/CODE_OF_CONDUCT.md).\n\n## License\n\n`dt-cli` is an Open Source Project. Please see\n[LICENSE](https://github.com/dynatrace-oss/dt-cli/blob/main/LICENSE) for more information.',
    'author': 'Wiktor Bachnik',
    'author_email': 'wiktor.bachnik@dynatrace.com',
    'maintainer': 'Wiktor Bachnik',
    'maintainer_email': 'wiktor.bachnik@dynatrace.com',
    'url': 'https://github.com/dynatrace-oss/dt-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
