from setuptools import setup, find_packages
from collections import OrderedDict

long_description="""
This is a fancy viewer for the Battlehack20 game.
Read more at the Battlehack website: https://bh2020.battlecode.org.
"""

setup(name='battlehack20-fancyviewer',
      version="1.1.0",
      description='Battlehack 2020 fancy viewer.',
      author='cooljoseph',
      long_description=long_description,
      author_email='camacho.joseph@gmail.com',
      url="https://bh2020.battlecode.org",
      license='GNU General Public License v3.0',
      packages=find_packages(),
      project_urls=OrderedDict((
          ('Code', 'https://github.com/cooljoseph1/battlehack20-fancyviewer'),
          ('Documentation', 'https://github.com/cooljoseph1/battlehack20-fancyviewer')
      )),
      install_requires=[
            'pillow==7.0.0'
      ],
      python_requires='>=3, <3.8',
      zip_safe=False,
      include_package_data=True
)
