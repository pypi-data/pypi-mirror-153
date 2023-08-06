# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mastodonamnesia']

package_data = \
{'': ['*']}

install_requires = \
['Mastodon.py>=1.5.1,<2.0.0',
 'alive-progress>=2.3.1,<3.0.0',
 'arrow>=1.2.1,<2.0.0',
 'httpx>=0.23.0,<0.24.0',
 'rich>=12.0.0,<13.0.0',
 'typing-extensions>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['mastodonamnesia = mastodonamnesia.mastodon_amnesia:main']}

setup_kwargs = {
    'name': 'mastodonamnesia',
    'version': '0.5.1',
    'description': 'deletes old Mastodon toots',
    'long_description': '# MastodonAmnesia\n\n***!!! BEWARE, THIS TOOL WILL DELETE SOME OF YOUR MASTODON TOOTS !!!***\n\nMastodonAmnesia is a command line (CLI) tool to help delete old toots from Mastodon. It respects rate limits imposed by\nMastodon servers.\n\nInstall MastodonAmnesia from Pypi using:\n`pip install mastodon_amnesia`\nand then run `mastodonamnesia`\n\nOr alternatively you can run MastodonAmnesia from [source][4] by cloning the repository using the following command line:\n`git clone https://codeberg.org/MarvinsMastodonTools/mastodonamnesia.git`\n\nAs MastodonAmnesia is now using [Poetry][1] for dependency control, please install Poetry before proceeding further.\n\nBefore running, make sure you have all required python modules installed. With [Poetry][1] this is as easy as:\n`poetry install --no-dev`\n\nMastodonAmnesia will ask for all necessary parameters when run for the first time and store them in `config.json`\nfile in the current directory.\n\nRun MastodonAmnesia with the command `poetry run mastodonamnesia`\n\n\nMastodonAmnesia is licences under licensed under\nthe [GNU Affero General Public License v3.0][2]\n\n## Supporting MastodonAmnesia\n\nThere are a number of ways you can support MastodonAmnesia:\n\n- Create an issue with problems or ideas you have with/for MastodonAmnesia\n- You can [buy me a coffee][3].\n- You can send me small change in Monero to the address below:\n\nMonero donation address:\n`86ZnRsiFqiDaP2aE3MPHCEhFGTeipdQGJZ1FNnjCb7s9Gax6ZNgKTyUPmb21WmT1tk8FgM7cQSD5K7kRtSAt1y7G3Vp98nT`\n\n[1]: https://python-poetry.org/\n[2]: http://www.gnu.org/licenses/agpl-3.0.html\n[3]: https://www.buymeacoffee.com/marvin8\n[4]: https://codeberg.org/MarvinsMastodonTools/mastodonamnesia\n',
    'author': 'marvin8',
    'author_email': 'marvin8@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://codeberg.org/MarvinsMastodonTools/mastodonamnesia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
