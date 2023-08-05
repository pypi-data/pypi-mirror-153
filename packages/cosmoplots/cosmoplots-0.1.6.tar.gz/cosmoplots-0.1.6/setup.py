# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cosmoplots']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2', 'numpy>=1.15.0']

setup_kwargs = {
    'name': 'cosmoplots',
    'version': '0.1.6',
    'description': 'Routines to get a sane default configuration for production quality plots.',
    'long_description': '# cosmoplots\n\nRoutines to get a sane default configuration for production quality plots. Used by complex systems modelling group at UiT.\n\n## Installation\n\nThe package is published to PyPI and can be installed with\n\n```sh\npip install cosmoplots\n```\n\nIf you want the development version you must first clone the repo to your local machine,\nthen install the project and its dependencies with [poetry]:\n\n```sh\ngit clone https://github.com/uit-cosmo/cosmoplots.git\ncd cosmoplots\npoetry install\n```\n\n## Usage\n\nSet your `rcparams` before plotting in your code, for example:\n\n```Python\nimport cosmoplots\n\naxes_size = cosmoplots.set_rcparams_dynamo(plt.rcParams, num_cols=1, ls="thin")\n```\n\n## `change_log_axis_base`\n\n```python\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport cosmoplots\n\naxes_size = cosmoplots.set_rcparams_dynamo(plt.rcParams, num_cols=1, ls="thin")\na = np.exp(np.linspace(-3, 5, 100))\nfig = plt.figure()\nax = fig.add_axes(axes_size)\nax.set_xlabel("X Axis")\nax.set_ylabel("Y Axis")\nbase = 2  # Default is 10, but 2 works equally well\ncosmoplots.change_log_axis_base(ax, "x", base=base)\n# Do plotting ...\n# If you use "plot", the change_log_axis_base can be called at the top (along with add_axes\n# etc.), but using loglog, semilogx, semilogy will re-set, and the change_log_axis_base\n# function must be called again.\nax.plot(a)\nplt.show()\n```\n\n## `matplotlib` vs. `cosmoplots` defaults\n\n```python\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport cosmoplots\n\n# Matplotlib --------------------------------------------------------------------------- #\na = np.exp(np.linspace(-3, 5, 100))\nfig = plt.figure()\nax = fig.add_subplot()\nax.set_xlabel("X Axis")\nax.set_ylabel("Y Axis")\nax.semilogy(a)\n# plt.savefig("assets/matplotlib.png")\nplt.show()\n\n# Cosmoplots --------------------------------------------------------------------------- #\naxes_size = cosmoplots.set_rcparams_dynamo(plt.rcParams, num_cols=1, ls="thin")\na = np.exp(np.linspace(-3, 5, 100))\nfig = plt.figure()\nax = fig.add_axes(axes_size)\nax.set_xlabel("X Axis")\nax.set_ylabel("Y Axis")\ncosmoplots.change_log_axis_base(ax, "y")\nax.semilogy(a)\n# Commenting out the below line result in the default base10 ticks\ncosmoplots.change_log_axis_base(ax, "y")\n# plt.savefig("assets/cosmoplots.png")\nplt.show()\n```\n\n| `matplotlib` | `cosmoplots` |\n| :--------: | :--------: |\n| ![matplotlib](./assets/matplotlib.png) | ![cosmoplots](./assets/cosmoplots.png) |\n\n<!-- Links -->\n[poetry]: https://python-poetry.org\n',
    'author': 'gregordecristoforo',
    'author_email': 'gregor.decristoforo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uit-cosmo/cosmoplots',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
