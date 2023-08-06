# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kdmapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kdmapi',
    'version': '1.0.1',
    'description': "KDMAPI (Keppy's Direct MIDI API) wrapper for Python",
    'long_description': '# kdmapi\n\n[KDMAPI (Keppy\'s Direct MIDI API)](https://github.com/KeppySoftware/OmniMIDI/blob/master/DeveloperContent/KDMAPI.md) wrapper for Python\n\nkdmapi provides both C bindings for OmniMIDI.dll and a Python-friendly wrapper for them\n\nA [Mido](https://pypi.org/project/mido/) backend is also provided, instructions on how to use it are below\n\n## Installation\n\n```sh\npip3 install kdmapi\n```\n\nYou will also need to have [OmniMIDI](https://github.com/KeppySoftware/OmniMIDI) installed\n\n## Instructions\n\n```python\nfrom kdmapi import KDMAPI\n\n# Initialize the device\nKDMAPI.InitializeKDMAPIStream()\n\n# Send a short 32-bit MIDI message data\nKDMAPI.SendDirectData(0x0)\n\n# Close the device\nKDMAPI.TerminateKDMAPIStream()\n```\n\n# Mido backend\n\nYou can use KDMAPI as a [Mido](https://pypi.org/project/mido/) output backend\n\n```python\nimport mido\n\n# Set KDMAPI as MIDO backend\nmido.set_backend("kdmapi.mido_backend")\n\n# Open MIDI file\nmidi_file = mido.MidiFile("your_file.mid")\n\nwith mido.open_output() as out:\n    for msg in midi_file.play():\n        out.send(msg)\n```\n\n# License\n\n```\n#\n# Copyright (C) 2022 Sebastiano Barezzi\n#\n# SPDX-License-Identifier: LGPL-3.0-or-later\n#\n```\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SebaUbuntu/kdmapi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
