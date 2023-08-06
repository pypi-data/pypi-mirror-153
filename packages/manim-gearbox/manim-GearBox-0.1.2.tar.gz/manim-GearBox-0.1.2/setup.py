# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_gearbox', 'manim_gearbox.gear_mobject']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.13.1', 'scipy']

entry_points = \
{'manim.plugins': ['manim_gearbox = manim_gearbox']}

setup_kwargs = {
    'name': 'manim-gearbox',
    'version': '0.1.2',
    'description': 'This is an extension of Manim that helps drawing nice looking gears.',
    'long_description': None,
    'author': 'GarryBGoode',
    'author_email': 'bgeri91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
