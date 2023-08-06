# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starship_landing_gym', 'starship_landing_gym.envs']

package_data = \
{'': ['*']}

install_requires = \
['gym==0.19.0',
 'numpy==1.21.5',
 'pyglet>=1.5.21,<2.0.0',
 'stable-baselines3>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'starship-landing-gym',
    'version': '0.1.2',
    'description': 'A Gym env for rocket landing.',
    'long_description': '# Starship Landing Gym [![tests](https://github.com/Armandpl/starship-landing-gym/actions/workflows/tests.yml/badge.svg)](https://github.com/Armandpl/starship-landing-gym/actions/workflows/tests.yml)\nA Gym env for propulsive rocket landing. \n\n<p align="center">\n  <img width="400" height="500" src="https://raw.githubusercontent.com/Armandpl/starship-landing-gym/master/images/landing.gif">\n  <br/>\n  <i> Successfull Rocket Landing </i>\n</p>\n\nThe goal is to bring the rocket above the landing pad with a speed inferior to 5m/s.  \n\nThis is inspired by and based on Thomas Godden\'s ["Starship Landing Trajectory Optimization" blog post.](http://thomasgodden.com/starship-trajopt.html)\n\n## Installation\n\n`pip install starship-landing-gym`\n\n## Usage\n\n```python\nimport gym\nimport starship_landing_gym\n\nenv = gym.make("StarshipLanding-v0")\n\ndone = False\nwhile not done:\n    action = ... # Your agent code here\n    obs, reward, done, info = env.step(action)\n    env.render()\n```\n\n## Obvervations and Actions\n\n<p align="center">\n  <img width="1280" height="720" src="https://raw.githubusercontent.com/Armandpl/starship-landing-gym/master/images/env_description.jpg">\n</p>\n',
    'author': 'Armandpl',
    'author_email': 'adpl33@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Armandpl/starship-landing-gym',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
