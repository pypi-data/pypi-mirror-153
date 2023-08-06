# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frameioclient', 'frameioclient.lib', 'frameioclient.resources']

package_data = \
{'': ['*']}

install_requires = \
['analytics-python>=1.4.0,<2.0.0',
 'enlighten>=1.10.2,<2.0.0',
 'importlib-metadata>=4.11.3,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'token-bucket>=0.3.0,<0.4.0',
 'urllib3>=1.26.9,<2.0.0',
 'xxhash>=3.0.0,<4.0.0']

entry_points = \
{'console_scripts': ['fiocli = frameioclient.fiocli:main']}

setup_kwargs = {
    'name': 'frameioclient',
    'version': '2.0.1a2',
    'description': 'Client library for the Frame.io API',
    'long_description': '# python-frameio-client\n\n[![PyPI version](https://badge.fury.io/py/frameioclient.svg)](https://badge.fury.io/py/frameioclient)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/frameioclient.svg)](https://pypi.python.org/pypi/frameioclient/)\n\n\n<img width="1644" alt="artboard_small" src="https://user-images.githubusercontent.com/19295862/66240171-ba8dd280-e6b0-11e9-9ccf-573a4fc5961f.png">\n\n# Frame.io \nFrame.io is a cloud-based collaboration hub that allows video professionals to share files, comment on clips real-time, and compare different versions and edits of a clip. \n\n## Overview\n\n### Installation\n\nvia Pip\n```\n$ pip install frameioclient\n```\n\nvia Source\n```\n$ git clone https://github.com/frameio/python-frameio-client\n$ pip install .\n```\n\n### Developing\nInstall the package into your development environment and link to it by running the following:\n\n```sh\npipenv install -e . -pre\n```\n\n## Documentation\n\n[Frame.io API Documentation](https://developer.frame.io/docs)\n\n### Use CLI\nWhen you install this package, a cli tool called `fioctl` will also be installed to your environment.\n\n**To upload a file or folder**\n```sh\nfioctl \\\n--token fio-u-YOUR_TOKEN_HERE  \\\n--destination "YOUR TARGET FRAME.IO PROJECT OR FOLDER" \\\n--target "YOUR LOCAL SYSTEM DIRECTORY" \\\n--threads 8\n```\n\n**To download a file, project, or folder**\n```sh\nfioctl \\\n--token fio-u-YOUR_TOKEN_HERE  \\\n--destination "YOUR LOCAL SYSTEM DIRECTORY" \\\n--target "YOUR TARGET FRAME.IO PROJECT OR FOLDER" \\\n--threads 2\n```\n\n### Links\n\n**Sphinx Documentation**\n- https://pythonhosted.org/sphinxcontrib-restbuilder/\n- https://www.npmjs.com/package/rst-selector-parser\n- https://sphinx-themes.org/sample-sites/furo/_sources/index.rst.txt\n- https://developer.mantidproject.org/Standards/DocumentationGuideForDevs.html\n- https://sublime-and-sphinx-guide.readthedocs.io/en/latest/code_blocks.html\n- https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html\n- https://stackoverflow.com/questions/64451966/python-sphinx-how-to-embed-code-into-a-docstring\n- https://pythonhosted.org/an_example_pypi_project/sphinx.html\n\n**Decorators**\n- https://docs.python.org/3.7/library/functools.html\n- https://realpython.com/primer-on-python-decorators/\n- https://www.sphinx-doc.org/en/master/usage/quickstart.html\n- https://www.geeksforgeeks.org/decorators-with-parameters-in-python/\n- https://stackoverflow.com/questions/43544954/why-does-sphinx-autodoc-output-a-decorators-docstring-when-there-are-two-decora\n\n\n## Usage\n\n_Note: A valid token is required to make requests to Frame.io. Go to our [Developer Portal](https://developer.frame.io/) to get a token!_\n\nIn addition to the snippets below, examples are included in [/examples](/examples).\n\n### Get User Info\n\nGet basic info on the authenticated user.\n\n```python\nfrom frameioclient import FrameioClient\n\nclient = FrameioClient("TOKEN")\nme = client.users.get_me()\nprint(me[\'id\'])\n```\n\n### Create and Upload Asset\n\nCreate a new asset and upload a file. For `parent_asset_id` you must have the root asset ID for the project, or an ID for a folder in the project. For more information on how assets work, check out [our docs](https://developer.frame.io/docs/workflows-assets/uploading-assets).\n\n```python\nimport os\nfrom frameioclient import FrameioClient\n\nclient = FrameioClient("TOKEN")\n\n\n# Create a new asset manually\nasset = client.assets.create(\n  parent_asset_id="1234abcd",\n  name="MyVideo.mp4",\n  type="file",\n  filetype="video/mp4",\n  filesize=os.path.getsize("sample.mp4")\n)\n\n# Create a new folder\nclient.assets.create(\n  parent_asset_id="",\n  name="Folder name",\n  type="folder" # this kwarg is what makes it a folder\n)\n\n# Upload a file \nclient.assets.upload(destination_id, "video.mp4")\n```\n',
    'author': 'Frame.io DevRel',
    'author_email': 'platform@frame.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Frameio/python-frameio-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
