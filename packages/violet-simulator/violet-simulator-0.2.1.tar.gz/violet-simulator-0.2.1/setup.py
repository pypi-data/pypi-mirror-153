# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vi']

package_data = \
{'': ['*']}

install_requires = \
['polars>=0.13.38,<0.14.0',
 'pygame>=2.1.2,<3.0.0',
 'pyserde[toml]>=0.7.3,<0.8.0',
 'typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'violet-simulator',
    'version': '0.2.1',
    'description': 'A smol simulator framework built on top of PyGame',
    'long_description': '# Violet\n\nA smol simulator framework built on top of [PyGame](https://www.pygame.org/docs/).\n\n- Automatic agent wandering behaviour\n- Fully deterministic simulations with PRNG seeds\n- Install Violet with a simple `pip install` 😎\n- Matrix-powered multi-threaded configuration testing\n- [Polars](https://github.com/pola-rs/polars/)-powered simulation analytics\n- Replay-able simulations with a ✨ time machine ✨\n- Type-safe configuration system (with TOML support)\n\nWant to get started right away?\nCheck out the [Violet Starter Kit](https://github.com/m-rots/violet-starter-kit)!\n\n## Installation\n\nInstall the latest version of Violet with:\n\n```bash\npip3 install -U violet-simulator\n```\n\nOr with [Poetry](https://python-poetry.org):\n\n```bash\npoetry add violet-simulator\n```\n\n## Example\n\n```python\nfrom vi import Agent, Simulation\n\n(\n    # Step 1: Create a new simulation.\n    Simulation()\n    # Step 2: Add 100 agents to the simulation.\n    .batch_spawn_agents(100, Agent, images=["examples/images/white.png"])\n    # Step 3: Profit! 🎉\n    .run()\n)\n```\n\nFor more information you can check the [documentation](https://api.violet.m-rots.com), [examples](https://github.com/m-rots/violet/tree/main/examples) and the [User Guide](https://violet.m-rots.com).',
    'author': 'Storm Timmermans',
    'author_email': 'stormtimmermans@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://violet.m-rots.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
