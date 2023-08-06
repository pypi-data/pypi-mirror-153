import re
from pathlib import Path

from setuptools import find_packages, setup


def load_requirements():
    """Return a list of package dependencies from the project requirements file"""

    with open('requirements.txt') as f:
        return f.read().splitlines()


def load_long_description():
    """Return the package description from the project readme"""

    with open('README.md') as f:
        return f.read()


def get_meta():
    """Return the package version and author as defined in the package __init__ file."""

    init_path = Path(__file__).resolve().parent / 'django_keygen/__init__.py'
    with init_path.open('r') as infile:
        init_content = infile.read()

    version_reg_exp = re.compile("__version__ = '(.*?)'")
    version = version_reg_exp.findall(init_content)[0]

    author_reg_exp = re.compile("__author__ = '(.*?)'")
    author = author_reg_exp.findall(init_content)[0]

    return version, author


_version, _author = get_meta()
setup(name='django-keygen',
      version=_version,
      author=_author,
      packages=find_packages(),
      long_description=load_long_description(),
      long_description_content_type='text/markdown',
      keywords='Django Secret Key',
      description='A secure secret key generator for Django',
      classifiers=[
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
      ],
      license='GPL v3',
      python_requires='>=3.6',
      install_requires=load_requirements(),
      include_package_data=True
      )
