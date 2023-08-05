'''Setup for the module'''

__author__ = 'Julian Stirling'
__version__ = '0.0.2'

import sys
from os import path
import glob
from setuptools import setup, find_packages

def install():
    '''The installer'''

    if sys.version_info[0] == 2:
        sys.exit("Sorry, Python 2 is not supported")

    static_files = glob.glob('kitdex/static/*', recursive=True)
    package_data_location = [static_file[7:] for static_file in static_files]
    templates = glob.glob('kitdex/templates/*', recursive=True)
    for template in templates:
        package_data_location.append(template[7:])


    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as file_id:
        long_description = file_id.read()
    short_description = ('An index for where to find your kit.')

    setup(name='kitdex',
          version=__version__,
          license="GPLv3",
          description=short_description,
          long_description=long_description,
          long_description_content_type='text/markdown',
          author=__author__,
          author_email='julian@julianstirling.co.uk',
          packages=find_packages(),
          package_data={'kitdex': package_data_location},
          keywords=['Organisation', 'Hardware'],
          zip_safe=False,
          project_urls={"Bug Tracker": "https://gitlab.com/julianstirling/kitdex/issues",
                        "Source Code": "https://gitlab.com/julianstirling/kitdex"},
          classifiers=['Development Status :: 5 - Production/Stable',
                       'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                       'Programming Language :: Python :: 3.6'],
          install_requires=['argparse',
                            'pyyaml>=5.1',
                            'marshmallow>=03.8,<3.12',
                            'jinja2',
                            'flask',
                            'requests',
                            'pywebview[qt]'],
          python_requires=">=3.6",
          entry_points={'console_scripts': ['kitdex = kitdex.__main__:main']})

if __name__ == "__main__":
    install()
