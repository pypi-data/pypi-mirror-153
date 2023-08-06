# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['de_workflow']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'datapane>=0.14.0,<0.15.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.7.0,<6.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.3.0,<13.0.0']

entry_points = \
{'console_scripts': ['de-workflow = de_workflow.main:app']}

setup_kwargs = {
    'name': 'de-workflow',
    'version': '0.2.0',
    'description': '',
    'long_description': '# DE Workflow\n\nThis is a small wrapper program around the [drug-extraction-cli](https://github.com/UK-IPOP/drug-extraction/tree/main/cli) program.\n\nIt is effectively a convenience wrapper for us and our typical use-case.\n\nBenefits over the standard CLI:\n\n- Multi-column support (it _expects_ two columns -- a primary and a secondary)\n- Wide form data created automatically\n- Wide form data attached to source data ready for analysis\n- Automated report generation\n- Use of either our/your custom search template _with tags!_\n\nIt can generate a nice report using [datapane](https://github.com/datapane/datapane) for some quick eye-ball analysis.\n\nIt uses `data/drug_info.json` ([link](data/drug_info.json)) as our template for custom search words **with tags**. This can be extended or edited where you can provide ANY custom search file you want as long as it matches our format. Alternatively you can enable `--live` mode and just use ours 🙂.\n\n- [DE Workflow](#de-workflow)\n  - [Requirements](#requirements)\n  - [Installation](#installation)\n  - [Usage](#usage)\n  - [Sample Output](#sample-output)\n  - [Support](#support)\n  - [Contributing](#contributing)\n  - [MIT License](#mit-license)\n\n## Requirements\n\n- [pipx](https://pypa.github.io/pipx/)\n- [drug-extraction-cli program](../cli/README.md)\n\n## Installation\n\nYou can install this program with [pipx](https://pypa.github.io/pipx/):\n\n```bash\npipx install de-workflow\n```\n\nYou can then easily get help for the only command (execute) like so:\n\n```bash\nde-workflow execute --help\n```\n\nWhich should look something like this:\n![help-screenshot](images/help-screenshot.png)\n\n## Usage\n\nTo run this tool all you will need to know is:\n\n- The name of your file\n- Your ID column for linking\n- Your Target column(s) to search in\n\nYou can then run the tool:\n\n```bash\nde-workflow execute ../cli/data/records.csv "Case Number" "Primary Cause" "Secondary Cause"\n```\n\nThis will run the underlying drug extraction program so you **MUST** have the main [CLI](https://github.com/UK-IPOP/drug-extraction/tree/main/cli) tool installed.\n\nThere are additional flags for reporting and custom file searching.\n\n`--report/--no-report` identifies whether or not to produce a `datapane` report at the end. Suggested and default value is `--report`.\n\n`--live/no-live` identifies whether or not you want you use our [template](data/drug_info.json).\n\nIf you do **NOT** want to use our template, you can disable live (`--no-live`) but you then MUST provide a custom `--search-file` for the program to use. This file should be in `json` format and match the structure of our template so that the tool can work correctly.\n\n## Sample Output\n\n![page1](images/page1.png)\n\n![page2](images/page2.png)\n\n## Support\n\nIf you encounter any issues or need support please either contact [@nanthony007](<[github.com/](https://github.com/nanthony007)>) or [open an issue](https://github.com/UK-IPOP/drug-extraction/issues/new).\n\n## Contributing\n\nContributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\nIf you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".\nDon\'t forget to give the project a star! Thanks again!\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md) for more details.\n\n## MIT License\n\n[LICENSE](LICENSE)\n',
    'author': 'Nick Anthony',
    'author_email': 'nanthony007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11.0',
}


setup(**setup_kwargs)
