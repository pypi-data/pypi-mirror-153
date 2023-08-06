# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['giradischi',
 'giradischi.backends',
 'giradischi.backends.alsamidi',
 'giradischi.backends.fluidsynth',
 'giradischi.backends.kdmapi',
 'giradischi.backends.portmidi',
 'giradischi.backends.rtmidi',
 'giradischi.ui',
 'giradischi.utils']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.2.4,<7.0.0', 'mido>=1.2.10,<2.0.0']

entry_points = \
{'console_scripts': ['giradischi = giradischi.main:main']}

setup_kwargs = {
    'name': 'giradischi',
    'version': '1.0.8',
    'description': 'GUI MIDI player supporting multiple backends',
    'long_description': '# giradischi\n\n[![PyPi version](https://img.shields.io/pypi/v/giradischi)](https://pypi.org/project/giradischi/)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c6d1edc8e4bc45a9b96eed73c55e3128)](https://www.codacy.com/gh/SebaUbuntu/giradischi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SebaUbuntu/giradischi&amp;utm_campaign=Badge_Grade)\n\nGUI MIDI player supporting multiple backends\n\nRequires Python 3.8 or greater\n\n## Installation\n\n```sh\npip3 install giradischi\n```\n\n### Backends\n\n-   ALSA MIDI: Install [alsa-midi](https://pypi.org/project/alsa-midi/) with `pip3 install alsa-midi` and follow the instructions provided [here](https://python-alsa-midi.readthedocs.io/en/latest/overview.html#installation)\n-   FluidSynth: Install [pyFluidSynth](https://pypi.org/project/pyFluidSynth/) with `pip3 install pyFluidSynth` and follow the instructions provided [here](https://github.com/nwhitehead/pyfluidsynth#requirements)\n-   KDMAPI: Install [kdmapi](https://pypi.org/project/kdmapi/) with `pip3 install kdmapi` and follow the instructions provided [here](https://github.com/SebaUbuntu/kdmapi)\n-   PortMidi: Follow the instructions provided [here](https://mido.readthedocs.io/en/latest/backends/portmidi.html)\n-   RtMidi: Install [python-rtmidi](https://pypi.org/project/python-rtmidi) with `pip3 install python-rtmidi` or install [rtmidi-python](https://pypi.org/project/rtmidi-python) with `pip3 install rtmidi-python`\n\n## How to use\n\n```sh\ngiradischi\n```\n\n```\n#\n# Copyright (C) 2022 Sebastiano Barezzi\n#\n# SPDX-License-Identifier: LGPL-3.0-or-later\n#\n```\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SebaUbuntu/giradischi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
