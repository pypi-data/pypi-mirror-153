# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_merger']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['file-merger = file_merger:main']}

setup_kwargs = {
    'name': 'file-merger',
    'version': '0.1.0rc2',
    'description': 'Merge multiple text files into one',
    'long_description': "# File merger\n\nMerge multiple files into one. Support inserting code as markdown code blocks.\n\n*Configuration file*\n\n| Key            | Description                                                                               | Default value |\n|:---------------|:------------------------------------------------------------------------------------------|:--------------|\n| files          | array with input files names <sup>1</sup>                                                 | -             |\n| folder         | sub-folder, where files located                                                           | -             |\n| output         | output file name with optional path, relative to config location                          | -             |\n| extension      | extension for all input and output files <sup>2</sup>                                     | -             |\n| add_file_names | add file name before its text, or not                                                     | `false`       |\n| file_label     | what write before file name                                                               | `File: `      |\n| remove_folder  | extract from 'folder/file.txt' only 'file.txt', for use in file name <sup>3</sup>         | `false`       |\n| code_in_md     | write code in markdown file between back-tics \\`\\`\\` with file extension for highlighting | `false`       |\n| ask_overwrite  | ask for overwrite or not                                                                  | `false`       |\n| empty          | generate empty file by path <sup>4</sup>                                                  | `false`       |\n| use            | use this config file or not                                                               | `true`        |\n\n<sup>1</sup> All the contents of the files are combined in the order of the files. In this list you can use key `text` instead of file name for inserting any text between file's content:\n\n```yaml\nfiles:\n  - text: 'some text'\n```\n\n<sup>2</sup> If specified, you should write the names of all files without extensions.\n\n<sup>3</sup> Used with the `add_file_names` flag enabled.\n\n<sup>4</sup> If specified, no other parameters are needed:\n\n```yaml\nempty: path/to/result/file\n```\n\n## Running\n\n```bash\npython path/to/file_merger.py -f FOLDER -c CONFIG_NAME\n```\n\n`-f` - Absolute path to folder with project, default is from where script run.\n\n`-c` - Config file name, default is `file-merger.yaml` (e.g. `folder/config.yaml`).\n",
    'author': 'Ilia',
    'author_email': 'istudyatuni@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/istudyatuni/file-merger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
