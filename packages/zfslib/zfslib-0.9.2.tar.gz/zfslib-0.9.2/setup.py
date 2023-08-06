# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zfslib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zfslib',
    'version': '0.9.2',
    'description': 'ZFS Utilities For Python3',
    'long_description': "# zfslib\n\nZFS Libraries for Python\n\nPython library for reading from ZFS Pools. Capable of reading, Pools, Datasets, Snapshots and Diffs for use by other Python Tools.\n\nThis tool presently targets Python v3.7+\n\n## Installation\n\nInstall this plugin using `pip`:\n\n    $ python3 -m pip install zfslib\n\n## Usage\n\nSee examples folder\n\n## Sample code\n\n```\n    import zfslib as zfs\n\n    # Read ZFS information from local computer\n    # For remote computer access, use certificate based ssh authentication \n    # see `examples/ex_remote.py`\n    conn = zfs.Connection(host='localhost')\n\n\n    # Load poolset. \n    # Properties can be queried here with: properties=['prop1','prop2',...]\n    # Default properties: name, creation\n    # If get_mounts=True, mountpoint and mounted are also retrieved automatically\n    # unlocking some functionality\n    # To see all available properties use: % zfs list -o foo\n    poolset = conn.load_poolset()\n\n    # Load a pool by name\n    pool = poolset.get_pool('dpool')\n    \n    # Get properties from ZFSItem's (Pool|DataSet|Snapshot)\n    # <ZFSItem>.get_property('<property>')\n    # -also-\n    # <ZFSItem>.path -> str: Full path for item\n    # <ZFSItem>.name -> str: Name of item\n    # <ZFSItem>.creation -> datetime\n    # <dataset>.mountpoint -> str\n    # <dataset|snapshot>.pool -> Pool\n    # <snapshot>.dataset -> DataSet\n    # <dataset>.dspath -> str: Dataset path excluding pool name\n    # <ZFSItem>.parent -> ZfsItem\n    # <pool|dataset>.children -> list(of ZfsItem)\n    # . Pools only contain DataSets\n    # . Datasets can contain DataSets and/or Snapshots\n\n\n    # Load dataset\n    ds = pool.get_dataset('vcmain')\n\n    # Load snapshots by with name of autosnap* that fall between \n    # the dates of 2020-12-20 and 2020-12-24\n    snapshots = ds.find_snapshots({\n        'name': 'autosnap*', 'date_from': '2020-12-20', 'date_to': '2020-12-24'\n    })\n\n    # Get all the changes file modification diffs for files that end with .py and .js \n    # excluding those in __pycache__ between the first and second snapshots\n    diffs = ds.get_diffs(\n         snapshots[0], snapshots[1]\n        ,file_type='F', chg_type='M'\n        ,include=['*.py', '*.js']\n        ,ignore=['*_pycache_*']\n    )\n\n    # Load snapshots by with name of autosnap* in the last 12 hours \n    snapshots = ds.find_snapshots({'name': 'autosnap*', 'tdelta': '12H'})\n\n    # Get Path to a file in the Snapshot folder (under mountpoint/.zfs/snapshots):\n    find_path = '<path_to_some_local_file_in_ZFS>'\n    (exists, snap_path) = snapshots[0].resolve_snap_path(find_path)\n    if exists:\n        print('snap_path: {}'.format(snap_path))\n    else: # file did not exist at time of snapshot creation\n        print('File not found in snapshot: {}'.format(find_path))\n\n```\n\n## Some Key Features\n### `<Dataset>.find_snapshots(dict)`\n```\n    # find_snapshots(dict) - Query all snapshots in Dataset\n    #  Options:\n    #  - name: Snapshot name (wildcard supported)\n    #  - contains: Path to resource (wildcard supported)\n    #  - dt_from: datetime to start\n    #  - tdelta: timedelta -or- string of nC where: n is an integer > 0 and C is one of y,m,d,H,M,S. Eg 5H = 5 Hours\n    #  - dt_to: datetime to stop \n    #  - index: (bool) - Return list(tuple(of int, snapshot, dataset)) where int is the index in current snaphot listing for dataset\n    #  Notes:\n    #  - Date searching is any combination of:\n    #      (dt_from --> dt_to) | (dt_from --> dt_from + tdelta) | (dt_to - tdelta --> dt_to) | (dt_from --> now)\n```\n\n### `<Dataset>.get_diffs()`\n```\n    # get_diffs() - Gets Diffs in snapshot or between snapshots (if snap_to is specified)\n    #               If snap_to is not specified, diff is to working copy\n    # snap_from - Left side of diff\n    # snap_to - Right side of diff. If not specified, diff is to current working version\n    # include - list of glob expressions to include (eg ['*_pycache_*'])\n    # exclude - list of glob expressions to exclude (eg ['*_pycache_*'])\n    # file_type - Filter on the following\n    #  - B       Block device\n    #  - C       Character device\n    #  - /       Directory\n    #  - >       Door\n    #  - |       Named pipe\n    #  - @       Symbolic link\n    #  - P       Event port\n    #  - =       Socket\n    #  - F       Regular file\n    # chg_type - Filter on the following:\n    #  - -       The path has been removed\n    #  - +       The path has been created\n    #  - M       The path has been modified\n    #  - R       The path has been renamed\n```\n\n### `<Snapshot>.snap_path`\n```\n    # Returns the path to read only zfs_snapshot directory (<ds_mount>/.zfs/snapshots/<snapshot>)\n```\n\n### `<Snapshot>.resolve_snap_path(path)`\n```\n    # Resolves the path to file/dir within the zfs_snapshot dir\n    # Returns: tuple(of bool, str) where:\n    # - bool = True if item is found\n    # - str = Path to item if found else path to zfs_snapshot dir\n```\n\n### `<Diff>.snap_path_left`\n```\n    # Path to resource on left side of diff in zfs_snapshot dir\n```\n\n### `<Diff>.snap_path_right`\n```\n    # Path to resource on right side of diff in .zfs_snapshot dir or working copy\n```\n\nSee `test.py` for more sample code\n\n\nCredits: This code is based heavily on [zfs-tools by Rudd-O](https://github.com/Rudd-O/zfs-tools).",
    'author': 'Timothy C. Quinn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/zfslib',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
