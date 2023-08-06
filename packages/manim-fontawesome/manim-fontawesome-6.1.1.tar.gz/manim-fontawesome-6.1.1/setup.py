# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_fontawesome']

package_data = \
{'': ['*'],
 'manim_fontawesome': ['font-awesome/*',
                       'font-awesome/svgs/brands/*',
                       'font-awesome/svgs/regular/*',
                       'font-awesome/svgs/solid/*']}

install_requires = \
['manim>=0.3']

entry_points = \
{'manim.plugins': ['manim_fontawesome = manim_fontawesome']}

setup_kwargs = {
    'name': 'manim-fontawesome',
    'version': '6.1.1',
    'description': "Font Awesome SVG's for Manim",
    'long_description': "# manim-fontawesome\n\nFont Awesome SVG's for Manim.\n\n## How to Use.\n\nYou can import this as any python library in your script and then use `brand`, `regular`, `solid` varaibles to get the necessary `SVGMobjects`.\n\nFor example,\n\n```py\nfrom manim import *\nfrom manim_fontawesome import *\n\nclass AngryEmoji(Scene):\n    def construct(self):\n        # import https://fontawesome.com/v5.15/icons/angry?style=regular\n        self.add(regular.angry)\n```\n\nThis module defined these variables:\n- `regular`: These contains the Regular Style icons.\n- `solid`: These contains the Solid style icons.\n- `brand`: These contains the Brands.\n\n# License\n\nThis module is licensed under BSD-3-Clause.\n",
    'author': 'Naveen M K',
    'author_email': 'naveen@manim.community',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/naveen521kk/manim-fontawesome',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
