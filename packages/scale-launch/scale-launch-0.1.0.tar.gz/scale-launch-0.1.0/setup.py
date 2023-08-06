# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['launch',
 'launch.cli',
 'launch.clientlib',
 'launch.clientlib.batching',
 'launch.clientlib.exe',
 'launch.clientlib.model_service',
 'launch.pipeline']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.0.0,<3.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=12.0.0,<13.0.0']

entry_points = \
{'console_scripts': ['scale-launch = launch.cli.bin:entry_point']}

setup_kwargs = {
    'name': 'scale-launch',
    'version': '0.1.0',
    'description': 'The official Python client library for Launch, the Data Platform for AI',
    'long_description': "# Launch Python Client\n```\n██╗      █████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗\n██║     ██╔══██╗██║   ██║████╗  ██║██╔════╝██║  ██║\n██║     ███████║██║   ██║██╔██╗ ██║██║     ███████║\n██║     ██╔══██║██║   ██║██║╚██╗██║██║     ██╔══██║\n███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╗██║  ██║\n╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝\n```\n\nMoving an ML model from experiment to production requires significant engineering lift.\nScale Launch provides ML engineers a simple Python interface for turning a local code snippet into a production service.\nA ML engineer needs to call a few functions from Scale's SDK, which quickly spins up a production-ready service.\nThe service efficiently utilizes compute resources and automatically scales according to traffic.\n\nLatest API/SDK reference can be found [here](https://scaleapi.github.io/launch-python-client/).\n\n## Deploying your model via Scale Launch\n\nCentral to Scale Launch are the notions of a `ModelBundle` and a `ModelEndpoint`.\nA `ModelBundle` consists of a trained model as well as the surrounding preprocessing and postprocessing code.\nA `ModelEndpoint` is the compute layer that takes in a `ModelBundle`, and is able to carry out inference requests\nby using the `ModelBundle` to carry out predictions. The `ModelEndpoint` also knows infrastructure-level details,\nsuch as how many GPUs are needed, what type they are, how much memory, etc. The `ModelEndpoint` automatically handles\ninfrastructure level details such as autoscaling and task queueing.\n\nSteps to deploy your model via Scale Launch:\n\n1. First, you create and upload a `ModelBundle`.\n\n2. Then, you create a `ModelEndpoint`.\n\n3. Lastly, you make requests to the `ModelEndpoint`.\n\nTODO: link some example colab notebook\n\n\n## For Developers\n\nClone from github and install as editable\n\n```\ngit clone git@github.com:scaleapi/launch-python-client.git\ncd launch-python-client\npip3 install poetry\npoetry install\n```\n\nPlease install the pre-commit hooks by running the following command:\n\n```bash\npoetry run pre-commit install\n```\n\n### Documentation\n\n**Updating documentation:**\nWe use [Sphinx](https://www.sphinx-doc.org/en/master/) to autogenerate our API Reference from docstrings.\n\nTo test your local docstring changes, run the following commands from the repository's root directory:\n\n```\npoetry shell\ncd src_docs\nsphinx-autobuild . ../docs --watch ../launch\n```\n\n`sphinx-autobuild` will spin up a server on localhost (port 8000 by default) that will watch for and automatically rebuild a version of the API reference based on your local docstring changes.\n",
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://scale.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
