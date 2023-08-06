# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ptpapi', 'ptpapi.scripts', 'ptpapi.sites']

package_data = \
{'': ['*']}

install_requires = \
['Tempita>=0.5.2,<0.6.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'bencode.py>=4.0.0,<5.0.0',
 'guessit>=3.4.3,<4.0.0',
 'humanize>=4.0.0,<5.0.0',
 'libtc>=1.3.1,<2.0.0',
 'pyrosimple>=1.1.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['ptp = ptpapi.scripts.ptp:main',
                     'ptp-reseed = ptpapi.scripts.ptp_reseed:main',
                     'ptp-reseed-machine = '
                     'ptpapi.scripts.ptp_reseed_machine:main']}

setup_kwargs = {
    'name': 'ptpapi',
    'version': '0.7.1',
    'description': 'A small API for a mildly popular movie site',
    'long_description': '# PTPAPI\n\nA small API for a mildly popular movie site. The goal was to be able to collect as much information in as few network requests as possible.\n\n## Dependencies\n\n* Python 3.7+\n* pip\n\n## Installation\n\nUse of a [virtualenv](https://virtualenv.readthedocs.org/en/latest/userguide.html#usage) is highly recommended.\n\n`pip install ptpapi`\n\n## Configuration\n\nOpen the file `~/.ptpapi.conf` for editing, and make sure it looks like the following:\n\n```ini\n[Main]\n\n[PTP]\nApiUser=<ApiUser>\nApiKey=<ApiKey>\n```\n\nBoth values can be found in the "Security" section of your profile. This is only the minimum required configuration. See `ptpapi.conf.example` for a full-futured config file with comments.\n\n## Usage\n\nThe three CLI commands are `ptp`, `ptp-reseed`, and `ptp-bookmarks`\n\n### `ptp`\n\nThis is a generally utility to do various things inside PTP. As of right now it can download files, search the site for movies, and list message in your inbox.\n\nSee `ptp help` for more information.\n\n#### `ptp inbox`\n\nA small utility to read messages in your inbox. No reply capability currently.\n\n#### `ptp download`\n\nAn alias for `ptp-search -d`\n\n#### `ptp search`\n\nThis subcommand lets you search the site for movies. It can take movie and permalinks, as well as search by arbitrary parameters, and the `-d` flag allows for downloading matching torrents. For instance: \n- `ptp search year=1980-2000 taglist=sci.fi`\n- `ptp search "Star Wars"`.\n\nIt can also accept URLs for torrents and collages:\n- `ptp search "https://passthepopcorn.me/torrents.php?id=68148"`\n- `ptp search "https://passthepopcorn.me/collages.php?id=2438"`\n\nand regular search URLs:\n- `ptp search "https://passthepopcorn.me/torrents.php?action=advanced&year=1980-2000&taglist=action"`.\n\nAs a general rule of thumb anything supported by the advanced site search will work with `ptp search`, e.g. searching `https://passthepopcorn.me/torrents.php?action=advanced&taglist=comedy&format=x264&media=Blu-ray&resolution=1080p&scene=1` is the same as `ptp search taglist=comedy format=x264 media=Blu-ray resolution=1080p scene=1`.\n\nTo work with multiple pages of results, use the `--pages <num>` flag.\n\nThere are a couple aliases to make life easier:\n\n* `genre`, `genres`, `tags` -> `taglist`\n* `name` -> `searchstr`\n* `bookmarks` -> Search only your bookmarks\n\nIn addition, [Tempita](http://pythonpaste.org/tempita/) can be used for custom formatting. For instance, `ptp search --movie-format="" --torrent-format="{{UploadTime}} - {{ReleaseName}}" year=1980-2000 taglist=sci.fi grouping=no`.\n\nUsing the `-d` flag will download one torrent from each of the matched torrents (deciding which one to download is done via [filters](#filters)) to the [downloadDirectory](ptpapi.conf.example#L9).\n\nThe `-p/--pages [int]` option can be used to scrape multiple pages at once. N.B.: If any `page` parameter is in the original search query, paging will start from that page.\n\n#### `ptp fields`\n\nSimply list fields that can be used for the `ptp search` formatting.\n\n### `ptp-reseed`\n\nThis script automatically matches up files to movies on PTP. It\'s most basic usage is `ptp-reseed <file path>`. This will search PTP for any movies matching that filename, and if it finds a match, will automatically download the torrent and add it to rtorrent. It can do some basic file manipulation if it finds a close enough match.\n\nFor instance, if you have the file `Movie.2000.mkv`, and the torrent contains `Movie (2000)/Movie.2000.mkv`, the script will try to automatically create the folder `Movie (2000)` and hard link the file inside of it before attempting to seed it.\n\nSee `ptp-reseed -h` and `ptpapi.conf.example` for more information and configuration options.\n\n#### guessit\n\nBy default the script looks for exact matches against file names and sizes. If you\'d like the name matching to be less strict, you can install the guessit library (`pip install \'guessit>=3\'`), and if the filename search fails, the script will attempt to parse the movie name out of the file with guessit.\n\n## Concepts\n\n### Filters\n\nFilters were designed as a way to take a full movie group, and narrow it down to a single torrent. A filter consists of multiple sub-filters, where the first sub-filter to match will download the torrent, and if not, the next sub-filter will be checked. If none of the sub-filters match, no download will occur. Filters are separate from the actual search parameters sent to the site\n\nThe full list of possible values for picking encodes is:\n* `GP` or `Scene`\n* `576p` or `720p` or `1080p`\n* `XviD` or `x264`\n* `HD` or `SD`\n* `remux` or `not-remux`\n* `seeded` - the number of seeds is greater than 0 (deprecated, use `seeders>0`)\n* `not-trumpable` - ignore any trumpable torrents\n* `unseen` - ignores all torrents if you\'ve marked the movie as seen or rated it\n* `unsnatched` - ignore all torrents unless you\'ve never snatched one before (note that seeding counts as "snatched", but leeching doesn\'t)\nThere are also values that allow for simple comparisons, e.g. `size>1400M`.\n* `seeders`\n* `size`\n\nNote that it\'s possible to have two incompatible values, e.g. `GP` and `Scene`, but this simply means the sub-filter won\'t ever match a torrent, and will always be skipped over.\n\nThe possible values for sorting are:\n* `most recent` (the default if none are specified)\n* `smallest`\n* `most seeders`\n* `largest`\n\n#### Examples\n\nFor instance, the filter `smallest GP,720p scene,largest` would attempt to download the smallest GP. If there are no GPs, it will try to find a 720p scene encode. If it can\'t find either of those, it will just pick the largest torrent available.\n\nAs another example, if you wanted to filter for encodes that are less than 200MiB with only one seeder, you could use `seeders=1 size<200M`.\n\n## Notes\n\nI did this mostly for fun and to serve my limited needs, which is why it\'s not as polished as it could be, and will probably change frequently.  Pull requests are welcomed.\n\n### Deprecated Configuration\n\nThe new ApiUser/ApiKey system is preferred, however if you find bugs or limitations, the old cookie-based method can be used as seen here.\n\nOpen the file `~/.ptpapi.conf` for editing, and make sure it looks like the following:\n\n```ini\n[Main]\n\n[PTP]\nusername=<username>\npassword=<password>\npasskey=<passkey>\n```\n',
    'author': 'kannibalox',
    'author_email': 'kannibalox@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kannibalox/PTPAPI',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
