# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itch_dl']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'lxml>=4.8.0,<5.0.0',
 'python-slugify>=6.1.2,<7.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'urllib3>=1.26.9,<2.0.0']

entry_points = \
{'console_scripts': ['itch-dl = itch_dl.cli:run']}

setup_kwargs = {
    'name': 'itch-dl',
    'version': '0.2.1',
    'description': 'itch.io bulk game downloader',
    'long_description': '# itch-dl\n\nBulk download games from [itch.io](https://itch.io/).\n\n- Can download game jams, browse pages (popular, newest, browse by tag...) and individual games.\n- Requires Python 3.8+, grab it from PyPI: `pip install itch-dl`\n- For development, use [Poetry](https://python-poetry.org/).\n\n\n## How to use\n\n- Log into itch.io with the account you\'d like to use for downloading.\n- Generate [a new API key](https://itch.io/user/settings/api-keys) on your user account page.\n- Check out which flags you can toggle: `itch-dl --help`\n- Run the downloader: `itch-dl --api-key <KEY> https://itch.io/jam/yourjamhere`\n- Wait. This is going to take a while.\n\nThe downloader is able to grab more or less everything you can download via the itch app.\n\nThe input URL can be any "Browse" page (top, popular, newest, filtered by tags, etc) or any\ngame jam. The input can also be a path to a itch.io JSON file with game jam entries, or just\na list of itch.io game URLs (not browse/jam pages!) to download.\n\n**It\'s expected that the downloader output will not be complete** - logs are stupidly verbose\nand it prints a report on failed downloads and external URLs (links to files that are not on\nitch.io itself, but rather on an external host like Google Drive, Dropbox, etc), so you must\nmanually grab whatever was not handled for you automatically.\n\nThe downloader also grabs the entry page HTML, which usually comes with controls and such. By\ndefault, it does not download images, assets and so on, just the text - use `--mirror-web` to\ntry and download these as well. This does not work very well yet, but gets the basics done.\n\n\n## Game Jam Entries JSON\n\nDownloader can parse and download games from a game jam entries JSON file if you need it.\n(The script basically automates the steps below, so if it\'s not able to do the same, please\ncreate an issue!)\n\n- Go to your jam\'s page, ex. https://itch.io/jam/gbcompo21 and right-click -> View Source.\n- Ctrl-F for `"id":` - it should find that text once, followed by a number. Write it down.\n- (It you found it multiple times, grab the one after I.ViewJam something something.)\n- Download https://itch.io/jam/ID/entries.json (replacing ID with what you wrote down).\n- Feed that to `itch-dl`!\n',
    'author': 'Dragoon Aethis',
    'author_email': 'dragoon@dragonic.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DragoonAethis/itch-dl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
