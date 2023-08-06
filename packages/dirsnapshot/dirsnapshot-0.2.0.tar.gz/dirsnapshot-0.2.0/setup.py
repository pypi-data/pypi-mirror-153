# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dirsnapshot']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['dirsnap = dirsnapshot.__main__:cli']}

setup_kwargs = {
    'name': 'dirsnapshot',
    'version': '0.2.0',
    'description': 'Report differences between a directory and a previous snapshot of the same directory.',
    'long_description': '# dirsnapshot\n\n## Description\n\nReport differences between a directory and a previous snapshot of the same directory.\n\nThis works very similar to [dircmp](https://docs.python.org/3/library/filecmp.html#the-dircmp-class) but it is designed to be used with a directory that is being monitored instead of comparing two existing directories.\n\nThis module can be run as a standalone CLI app as `dirsnap` or included in your project as a package.\n\n## Usage\n\n```python\nfrom dirsnapshot import DirDiff, create_snapshot\n\n# snapshot a directory\ncreate_snapshot("/Users/user/Desktop", "/Users/user/Desktop/Desktop.snapshot")\n\n# do some work\n...\n\n# compare the current state of the director to the snapshot\ndirdiff = DirDiff("/Users/user/Desktop/Desktop.snapshot", "/Users/user/Desktop")\n\n# print report to stdout\ndirdiff.report()\n\n# or print report to json\nprint(dirdiff.json())\n```\n\n## Installation\n\n```bash\npip install dirsnapshot\n```\n\n## CLI\n\nInstalling the `dirsnapshot` package will install a command line tool called `dirsnap` that can be used to create snapshots of directories and compare a directory to an existing snapshot.\n\n```\nusage: dirsnap [-h] [--json] [--snapshot DIRECTORY SNAPSHOT_FILE]\n               [--diff SNAPSHOT_A DIRECTORY_OR_SNAPSHOT_B]\n               [--descr DESCRIPTION] [--identical] [--ignore REGEX]\n               [--no-walk]\n\nCompare a directory to a previously saved snapshot or compare two directory\nsnapshots. You must specify one of --snapshot or --diff. Will show files\nadded/removed/modified. Files are considered modified if any of mode, uid,\ngid, size, or mtime are different.\n\noptions:\n  -h, --help            show this help message and exit\n  --json, -j            Output as JSON\n  --snapshot DIRECTORY SNAPSHOT_FILE, -s DIRECTORY SNAPSHOT_FILE\n                        Create snapshot of DIRECTORY at SNAPSHOT_FILE\n  --diff SNAPSHOT_A DIRECTORY_OR_SNAPSHOT_B\n                        Diff SNAPSHOT_A and DIRECTORY_OR_SNAPSHOT_B\n  --descr DESCRIPTION, -d DESCRIPTION\n                        Optional description of snapshot to store with\n                        snapshot for use with --snapshot.\n  --identical, -I       Include identical files in report (always included\n                        with --json)\n  --ignore REGEX, -i REGEX\n                        Ignore files matching REGEX\n  --no-walk             Don\'t walk directories\n```\n\nFor example:\n\n```bash\n$ dirsnap --snapshot ~/Desktop/export before.snapshot\nCreating snapshot of \'/Users/username/Desktop/export\' at \'before.snapshot\'\nSnapshot created at \'before.snapshot\'\n\n$ touch ~/Desktop/export/IMG_4548.jpg\n$ rm ~/Desktop/export/IMG_4547.jpg\n$ touch ~/Desktop/export/new_file.jpg\n\n$ dirsnap --diff before.snapshot ~/Desktop/export\ndiff \'/Users/username/Desktop/export\' 2022-06-05T18:38:11.189886 (Snapshot created at 2022-06-05T18:38:11.189886) vs 2022-06-05T18:39:07.225374 (Snapshot created at 2022-06-05T18:39:07.225374)\n\nAdded:\n    /Users/username/Desktop/export/new_file.jpg\n\nRemoved:\n    /Users/username/Desktop/export/IMG_4547.jpg\n\nModified:\n    /Users/username/Desktop/export/IMG_4548.jpg\n```\n\n## File Comparison\n\nDuring the `diff` comparison, files are considered equal if all properties of the file are equal. Currently, the properties checked are: is_file, is_dir, mode, uid, gid, size, mtime. If any of these properties are different, the file is considered modified.\n\n## File Format\n\nThe snapshot database file is a standard SQLite database.  The current schema is:\n\n```sql\nCREATE TABLE snapshot (\n                path TEXT,\n                is_dir INTEGER,\n                is_file INTEGER,\n                st_mode INTEGER,\n                st_uid INTEGER,\n                st_gid INTEGER,\n                st_size INTEGER,\n                st_mtime INTEGER);\nCREATE TABLE _metadata (\n                description TEXT, source TEXT, version TEXT, created_at DATETIME);\nCREATE TABLE about (\n                description TEXT, directory TEXT, datetime DATETIME);\nCREATE INDEX snapshot_path_index ON snapshot (path);\n```\n\nYou should not need access the database directly however, as the `DirSnapshot` class provides methods to access the necessary information abstracted from the actual database schema.\n',
    'author': 'Rhet Turnbull',
    'author_email': 'rturnbull+git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RhetTbull/dirsnapshot',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
