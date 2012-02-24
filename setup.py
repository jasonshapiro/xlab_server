__author__="thejo"
__date__ ="$Oct 12, 2010 11:58:35 PM$"

from setuptools import setup,find_packages

setup (
  name = 'ModeChoice',
  version = '0.1',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  install_requires=['foo>=3'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'thejo',
  author_email = 'thejo@berkeley.edu',

  summary = 'Mode Choice @ Berkeley',
  url = '',
  license = '',
  long_description= 'Application for the Mode Choice research project at the Systems Engineering department at UC Berkeley',

  # could also include long_description, download_url, classifiers, etc.

  
)