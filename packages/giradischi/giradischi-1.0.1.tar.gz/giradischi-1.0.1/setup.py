# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['giradischi',
 'giradischi.backends',
 'giradischi.backends.alsamidi',
 'giradischi.backends.fluidsynth',
 'giradischi.backends.portmidi',
 'giradischi.backends.rtmidi',
 'giradischi.ui',
 'giradischi.utils']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.2.4,<7.0.0', 'mido>=1.2.10,<2.0.0']

setup_kwargs = {
    'name': 'giradischi',
    'version': '1.0.1',
    'description': 'GUI MIDI player supporting multiple backends',
    'long_description': '# giradischi\n\n[![PyPi version](https://img.shields.io/pypi/v/giradischi)](https://pypi.org/project/giradischi/)\n\nGUI MIDI player supporting multiple backends\n\nRequires Python 3.9\n\n## Installation\n\n```sh\npip3 install giradischi\n```\n\n### Backends\n\n-   ALSA MIDI: Install [alsa-midi](https://pypi.org/project/alsa-midi/) with `pip3 install alsa-midi` and follow the instructions provided [here](https://python-alsa-midi.readthedocs.io/en/latest/overview.html#installation)\n-   FluidSynth: Install [pyFluidSynth](https://pypi.org/project/pyFluidSynth/) with `pip3 install pyFluidSynth` and follow the instructions provided [here](https://github.com/nwhitehead/pyfluidsynth#requirements)\n-   PortMidi: Follow the instructions provided [here](https://mido.readthedocs.io/en/latest/backends/portmidi.html)\n-   RtMidi: Install [python-rtmidi](https://pypi.org/project/python-rtmidi) with `pip3 install python-rtmidi` or install [rtmidi-python](https://pypi.org/project/rtmidi-python) with `pip3 install rtmidi-python`\n\n## How to use\n\n```sh\npython3 -m giradischi\n```\n\n```\n#\n# Copyright (C) 2022 Sebastiano Barezzi\n#\n# SPDX-License-Identifier: LGPL-3.0-or-later\n#\n```\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SebaUbuntu/giradischi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
