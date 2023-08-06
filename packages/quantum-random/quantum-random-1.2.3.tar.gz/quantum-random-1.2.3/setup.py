# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qrandom']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'xdg>=5.1.1,<6.0.0']

extras_require = \
{'numpy:python_version >= "3.7" and python_version < "3.10"': ['numpy>=1.17,<2.0',
                                                               'randomgen>=1.21.2,<2.0.0']}

entry_points = \
{'console_scripts': ['qrandom-init = qrandom._cli:init']}

setup_kwargs = {
    'name': 'quantum-random',
    'version': '1.2.3',
    'description': 'Quantum random numbers',
    'long_description': "# Quantum random numbers in Python\n\n![Tests](https://github.com/sbalian/quantum-random/workflows/Tests/badge.svg)\n\nThis package brings the [ANU quantum random numbers][anu] to Python 3.7 to 3.10.\n\nThe default pseudo-random generator in Python is replaced by calls to the\nANU API that serves real quantum random numbers.\n\n## Install\n\n```bash\npip install quantum-random\n```\n\nOptionally, for [NumPy][numpy] support,\n\n```bash\npip install quantum-random[numpy]\n```\n\nNote that the NumPy integration is not well-tested and is not available\nfor Python 3.10.\n\n## Setup: passing your API key\n\nANU now requires you to use an API key. You can get a free (trial) or paid key\nfrom [here][anupricing].\n\nYou can pass your key to `qrandom` in three ways:\n\n1. By setting the environment variable `QRANDOM_API_KEY`.\n2. By running `qrandom-init` to save your key in an INI config file that is\nstored in a subdirectory of your default home config directory (as specified\nby XDG, e.g., `/home/<your-username>/.config/qrandom/`).\n3. By running `qrandom-init` to save your key in an INI file in a directory\nof your choice set by `QRANDOM_CONFIG_DIR`.\n\n`qrandom` will look for the key in the order above. The `qrandom-init` utility\nis interactive and comes installed with `qrandom`.\n\n## Usage\n\nJust import `qrandom` and use it like you'd use the\n[standard Python random module][pyrandom]. For example,\n\n```python\n>>> import qrandom\n\n>>> qrandom.random()\n0.15357449726583722\n\n>>> qrandom.sample(range(10), 2)\n[6, 4]\n\n>>> qrandom.gauss(0.0, 1.0)\n-0.8370871276247828\n```\n\nAlternatively, you can `import QuantumRandom from qrandom` and use the class\ndirectly (just like `random.Random`).\n\nUnder the hood, batches of quantum numbers are fetched from the API as needed\nand each batch contains 1024 numbers. If you wish to pre-fetch more, use\n`qrandom.fill(n)`, where `n` is the number of batches.\n\nOptionally, if you have installed the NumPy integration,\n\n```python\n>>> from qrandom.numpy import quantum_rng\n\n>>> qrng = quantum_rng()\n\n>>> qrng.random((3, 3))  # use like numpy.random.default_rng()\narray([[0.37220278, 0.24337193, 0.67534826],\n       [0.209068  , 0.25108681, 0.49201691],\n       [0.35894084, 0.72219929, 0.55388594]])\n```\n\n## Tests\n\nTo run the tests locally, you will need [poetry][poetry] and Python 3.7-3.10.\nOne way of having multiple Python versions is to use [pyenv][pyenv] and list\nthe versions in `.python-version`. First, make sure you have set up your key.\nThen,\n\n```bash\npoetry install\npoetry run tox\n```\n\nSee [here](./docs/uniform.md) for a visualisation and a Kolmogorov–Smirnov test.\n\n## Notes on implementation\n\nThe `qrandom` module exposes a class derived from `random.Random` with a\n`random()` method that outputs quantum floats in the range [0, 1)\n(converted from 64-bit ints). Overriding `random.Random.random`\nis sufficient to make the `qrandom` module behave mostly like the\n`random` module as described in the [Python docs][pyrandom]. The exceptions\nat the moment are `getrandbits()` and `randbytes()` that are not available in\n`qrandom`. Because `getrandbits()` is not available, `randrange()` cannot\nproduce arbitrarily long sequences. Finally, the user is warned when `seed()`\nis called because there is no state. For the same reason, `getstate()` and\n`setstate()` are not implemented.\n\nNumPy support is provided using [RandomGen][randomgen].\n\n## License\n\nSee [LICENCE](./LICENSE).\n\n[anu]: https://quantumnumbers.anu.edu.au\n[anupricing]: https://quantumnumbers.anu.edu.au/pricing\n[pyrandom]: https://docs.python.org/3.9/library/random.html\n[poetry]: https://python-poetry.org\n[pyenv]: https://github.com/pyenv/pyenv\n[numpy]: https://numpy.org\n[randomgen]: https://github.com/bashtage/randomgen",
    'author': 'Seto Balian',
    'author_email': 'seto.balian@gmail.com',
    'maintainer': 'Seto Balian',
    'maintainer_email': 'seto.balian@gmail.com',
    'url': 'https://github.com/sbalian/quantum-random',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
