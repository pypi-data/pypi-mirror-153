# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autopilot',
 'autopilot.agents',
 'autopilot.data',
 'autopilot.data.interfaces',
 'autopilot.data.modeling',
 'autopilot.data.models',
 'autopilot.data.units',
 'autopilot.external',
 'autopilot.gui',
 'autopilot.gui.menus',
 'autopilot.gui.plots',
 'autopilot.gui.widgets',
 'autopilot.hardware',
 'autopilot.networking',
 'autopilot.setup',
 'autopilot.stim',
 'autopilot.stim.sound',
 'autopilot.stim.visual',
 'autopilot.tasks',
 'autopilot.transform',
 'autopilot.utils',
 'autopilot.viz']

package_data = \
{'': ['*']}

install_requires = \
['blosc2>=0.2.0,<0.3.0',
 'cffi>=1.15.0,<2.0.0',
 'inputs>=0.5,<0.6',
 'npyscreen>=4.10.5,<5.0.0',
 'numpy>=1.20.0,<2.0.0',
 'parse>=1.19.0,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pyzmq>=22.3.0,<23.0.0',
 'requests>=2.26.0,<3.0.0',
 'scikit-video>=1.1.11,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'tables>=3.7.0,<4.0.0',
 'tornado>=6.1.0,<7.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'validators>=0.18.2,<0.19.0']

extras_require = \
{':extra == "docs" or extra == "tests"': ['rich>=11.2.0,<12.0.0'],
 ':python_version < "3.8"': ['pandas>=1.3.0,<1.4.0',
                             'pip>=21.0.0,<22.0.0',
                             'importlib-metadata>=4.9.0,<5.0.0',
                             'typing-extensions>=4.1.1,<5.0.0'],
 ':python_version >= "3.8" and python_version < "3.10"': ['pandas>=1.4.0,<2.0.0'],
 'docs': ['pyqtgraph>=0.12.3,<0.13.0',
          'PySide2>=5.15.2,<6.0.0',
          'Sphinx>=4.3.1,<5.0.0',
          'autodocsumm>=0.2.7,<0.3.0',
          'matplotlib>=3.5.1,<4.0.0',
          'sphinxcontrib-bibtex>=2.4.1,<3.0.0',
          'scikit-learn>=1.0.1,<2.0.0',
          'altair>=4.1.0,<5.0.0',
          'bokeh>=2.4.2,<3.0.0',
          'colorcet>=3.0.0,<4.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'autodoc_pydantic>=1.7.0,<2.0.0',
          'myst_parser>=0.17.2,<0.18.0',
          'pytest>=7.0.0,<8.0.0'],
 'extra_interfaces': ['datajoint-babel>=0.1.9,<0.2.0',
                      'pynwb>=2.0.0,<3.0.0,!=2.5.1'],
 'pilot': ['JACK-Client>=0.5.3,<0.6.0'],
 'plotting': ['altair>=4.1.0,<5.0.0',
              'bokeh>=2.4.2,<3.0.0',
              'colorcet>=3.0.0,<4.0.0'],
 'terminal': ['pyqtgraph>=0.12.3,<0.13.0', 'PySide2>=5.15.2,<6.0.0'],
 'tests': ['pyqtgraph>=0.12.3,<0.13.0',
           'PySide2>=5.15.2,<6.0.0',
           'pytest>=7.0.0,<8.0.0',
           'pytest-cov>=3.0.0,<4.0.0',
           'pylint>=2.12.2,<3.0.0',
           'coveralls>=3.3.1,<4.0.0',
           'pytest-qt>=3.3.0,<3.4.0']}

setup_kwargs = {
    'name': 'auto-pi-lot',
    'version': '0.5.0a0',
    'description': 'Distributed behavioral experiments',
    'long_description': '![PyPI](https://img.shields.io/pypi/v/auto-pi-lot)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/auto-pi-lot)](https://pypi.org/project/auto-pi-lot/)\n![PyPI - Status](https://img.shields.io/pypi/status/auto-pi-lot)\n[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md) \n[![Twitter Follow](https://img.shields.io/twitter/follow/auto_pi_lot?style=social)](https://twitter.com/auto_pi_lot)\n\n\nStatus:\n\n[![Documentation Status](https://readthedocs.org/projects/auto-pi-lot/badge/?version=latest)](https://docs.auto-pi-lot.com/en/latest/?badge=latest)\n[![Travis (.com) branch](https://img.shields.io/travis/com/auto-pi-lot/autopilot/main)](https://app.travis-ci.com/github/auto-pi-lot/autopilot/branches)\n[![Coverage Status](https://coveralls.io/repos/github/auto-pi-lot/autopilot/badge.svg?branch=main)](https://coveralls.io/github/auto-pi-lot/autopilot?branch=main)\n![Jonny Status](https://img.shields.io/badge/jonny-dissertating-critical)\n\n\n\n# Autopilot\n\n![Autopilot Banner Logo](docs/_images/autopilot_logo_banner.png)\n\n| [Docs](https://docs.auto-pi-lot.com) | [Paper](https://www.biorxiv.org/content/10.1101/807693v1) | [Forum](https://github.com/auto-pi-lot/autopilot/discussions) | [Wiki](https://wiki.auto-pi-lot.com) |\n| :-: | :-: | :-: | :-: |\n| [![Read the Docs](docs/_images/docs_link.png)](https://docs.auto-pi-lot.com) | [![Paper](docs/_images/paper_link.png)](https://www.biorxiv.org/content/10.1101/807693v1)  | [![Forum](docs/_images/discussion_link.png)](https://github.com/auto-pi-lot/autopilot/discussions) | [![Wiki](docs/_images/hardware_link.png)](https://wiki.auto-pi-lot.com)\n\nAutopilot is a Python framework for performing complex, hardware-intensive behavioral experiments with swarms of networked Raspberry Pis. \nAs a tool, it provides researchers with a toolkit of flexible modules to design experiments without rigid programming & API limitations. \nAs a vision, it dreams of bridging the chaotic hacky creativity of scientific programmers with a standardized, \ncommunally developed library of reproducible experiment prototypes.\n\nAutopilot was developed with three primary design principles:\n\n* **Flexibility** - Autopilot was designed for any hardware and any experiment -- \n  its hardware API is designed to give a structured wrapper around the code you already use, and its task design is\n  entirely non-prescriptive. It attempts to eliminate the need for researchers to use a patchwork of mutually incompatible tools to perform complex\n  experiments. Autopilot is a hacker\'s plaything -- rather than a uniform, simplified experience,\n  its modular design and complete API-level documentation is meant to encourage users to make and break core Autopilot modules.\n* **Efficiency** - Autopilot uses Python as a glue around high-performance, low-level libraries,\n  and is fully concurrent across multiple threads, processes, and computers. Its distributed\n  design eliminates the hard limits faced by by single-computer\n  systems, letting researchers use arbitrary numbers and combinations of hardware components\n  to perform complex, hardware-intensive experiments at scale.\n* **Reproducibility** - Autopilot obsessively documents data provenance,\n  logging the entire history of an Animal\'s training, including any version and local\n  code changes. Any part of an experiment that isn\'t documented is considered a bug. By integrating experiments and producing data that is\n  clean at the time of acquisition, Autopilot makes it easy to do good science -- its goal is to allow\n  exact experimental replication from a single file. \n  \n\n# Distributed Behavior\n\nAutopilot\'s premise is simple: to scale experiments, *just use more computers*.\n\nAutopilot systems consist of multiple "Agents" -- computers with specialized roles in the swarm.\nOne user-facing "Terminal" agent allows a researcher to control many "Pilots," or computers that perform experiments (typically the beloved Raspberry Pi).\nEach Pilot can coordinate one or many "Children" to offload subsets of an experiment\'s computational or hardware requirements.\nUsers can use and misuse Autopilot\'s flexible modules to make whatever agent topology they need <3. \n\n![Autopilot System Diagram](docs/_images/whole_system_black.png)\n\n# Module Overview\n\nAutopilot divides the logical structure of experiments into independent<sup>1</sup> modules:\n\n| | Module |\n| :-: | --- |\n| ![Hardware](docs/_images/icon_agent.png) | **Agents - [Pilot](https://docs.auto-pi-lot.com/en/latest/autopilot.core.pilot.html) & [Terminal](https://docs.auto-pi-lot.com/en/latest/autopilot.core.terminal.html)** Runtime classes that encapsulate a computer/Pi\'s role in the swarm. Terminals provide the user interface and coordinate subjects and tasks, Pilots do the experiments. Formalizing the Agent API to allow additional agents like Compute or Surveillance agents is a major short-term development goal! |\n| ![Hardware](docs/_images/icon_hardware.png) | **[Hardware](https://docs.auto-pi-lot.com/en/latest/autopilot.hardware.html)** - Control your tools! Extensible classes to control whatever hardware you\'ve got. |\n| ![Hardware](docs/_images/icon_stim.png) | **[Stimuli](https://docs.auto-pi-lot.com/en/latest/autopilot.stim.html)** - Stimulus management and presentation. Parametric sound generation with a realtime audio server built on Jackd. Stubs are present for future development of visual stimuli using Psychopy. |\n| ![Hardware](docs/_images/icon_task.png) | **[Tasks](https://docs.auto-pi-lot.com/en/latest/autopilot.tasks.html)** - Build experiments! Write some basic metadata to describe data, plots, and hardware and the rest is up to you :)  |\n| ![Hardware](docs/_images/icon_data.png) | **[Subject](https://docs.auto-pi-lot.com/en/latest/autopilot.core.subject.html)** - Data management with hdf5 and pyTables. Abstraction layer for keeping obsessive records of subject history and system configuration |\n| ![Hardware](docs/_images/icon_transform.png) | **[Transforms](https://docs.auto-pi-lot.com/en/latest/autopilot.transform.html)** - Composable data transformations. Need to control the pitch of a sound with a video? build a transformation pipeline to connect your objects |\n| ![Hardware](docs/_images/icon_gui.png) | **[UI](https://docs.auto-pi-lot.com/en/latest/autopilot.core.gui.html)** - UI for controlling swarms of Pilots using Qt5/PySide2 |\n| ![Hardware](docs/_images/icon_viz.png) | **[Visualization](https://docs.auto-pi-lot.com/en/latest/autopilot.viz.html)** - (Mostly Prototypes) to do common visualizations |\n\n\n\n<sup>1</sup> a continual work in progress!\n# Getting Started\n\n[**All documentation is hosted at https://docs.auto-pi-lot.com**](https://docs.auto-pi-lot.com)\n\nInstallation is simple, just install with pip and use Autopilot\'s guided setup to configure your environment and preferences.\nThe initial setup routine uses a CLI interface that is SSH friendly :)\n\n```bash\npip3 install auto-pi-lot\npython3 -m autopilot.setup.setup\n```\n\n![Autopilot Setup Console](docs/_images/installer.png)\n\nAll of Autopilot is quite new, so bugs, incomplete documentation, missing features are very much expected! Don\'t be shy about\n[raising issues](https://github.com/auto-pi-lot/autopilot/issues) or [asking questions in the forum](https://github.com/auto-pi-lot/autopilot/discussions).\n\n\n# Development Status\n\nJonny is trying to graduate! Autopilot will be slow and maybe a little chaotic until then!\n\n## Branch Map\n\nWe\'re working on a formal contribution system, pardon the mess! Until we get that and our CI coverage up, `main` will lag a bit behind the development branches:\n\n* [`dev`](https://github.com/auto-pi-lot/autopilot/tree/dev) - main development branch that collects hotfixes, PRs, etc. Unstable but usually has lots of extra goodies\n* [`hotfix`](https://github.com/auto-pi-lot/autopilot/tree/hotfix) - branches from `dev` for building and testing hotfixes, PRs back to `dev`.\n* [`lab`](https://github.com/auto-pi-lot/autopilot/tree/lab) - branches from `dev` but doesn\'t necessarily PR back, the local branch used in the maintaining ([Wehr](http://uoneuro.uoregon.edu/wehr/)) lab\n* [`parallax`](https://github.com/auto-pi-lot/autopilot/tree/parallax) - experimental departure from `dev` to implement a particular experiment and rebuild a lot of components along the way, will eventually return to `dev` <3\n\n## Short-Term\n\nSee the short-term development goals in our version milestones:\n\n* [`v0.4.0`](https://github.com/auto-pi-lot/autopilot/milestone/1) - Implement registries to separate user code extensions like tasks and local hardware devices in a user directory, preserve source code in produced data so local development isn\'t lost. \n* [`v0.5.0`](https://github.com/auto-pi-lot/autopilot/milestone/2) - Make a unitary inheritance structure from a root Autopilot object such that a) common operations like logging and networking are implemented only once, b) the plugin system for `v0.4.0` can not only add new objects, but replace core objects while maintaining provenance (ie. no monkey patching needed), c) object behavior that requires coordination across multiple instances gets much easier, making some magical things like self-healing self-discovering networking possible. This will also include a major refactoring of the code structure, finally breaking up some of the truly monstrous thousand-line modules in `core` into an actually modular system we can build from <3\n\n## Long-Term\n\nAutopilot\'s extended development goals, in their full extravagance, can be found at the [Autopilot Development Todo](https://docs.auto-pi-lot.com/en/latest/todo.html)\n\n# What\'s new?\n\n**[v0.3.0](https://docs.auto-pi-lot.com/en/latest/changelog/v0.3.0.html#changelog-v030)**\n\nAfter much ado, we\'re releasing Autopilot\'s first major upgrade. Cameras, Continuous data, DeepLabCut, and a lot more!\n\n- Autopilot has moved to Python 3!! (Tested on 3.6-3.8)\n- Capturing video with OpenCV and the Spinnaker SDK is now supported (See autopilot.hardware.cameras)\n- An I2C_9DOF motion sensor and the MLX90640 temperature sensor are now supported.\n- Timestamps from GPIO events are now microsecond-precise thanks to some modifications to the pigpio library\n- GPIO output timing is also microsecond-precise thanks to the use of pigpio scripts, so you can deliver exactly the reward volumes you intend <3\n- Hardware modules have been refactored into their own module, and have been almost wholly rebuilt to have sensible inheritance structure.\n- Networking modules are more efficient and automatically compress arrays (like video frames!) on transmission. Streaming is also easier now, check out Net_Node.get_stream() !\n- We now have a detailed development roadmap , so you can see the magnificent future we have planned.\n- We have created the autopilot-users discussion board for troubleshooting & coordinating community development :)\n\n\n# Supported Systems\n\n**OS**\n\n- Ubuntu >=16.04\n- raspiOS >=Buster\n\n**Python Versions**\n\n- 3.7\n- 3.8\n- 3.9\n\n**Raspberry Pi Versions**\n\n- Raspi>=3b (Raspi 4 strongly recommended!)\n',
    'author': 'Jonny Saunders',
    'author_email': 'j@nny.fyi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://docs.auto-pi-lot.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
