__author__="dvizzini"
__date__ ="$2012-03-31 14:12:54.046304"

from setuptools import setup,find_packages

setup (
  name = 'XLab - Mobile',
  version = '0.1',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  install_requires=['foo>=3'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'dvizzini',
  author_email = 'dvizzini@gmail.com',

  summary = 'XLab - Mobile @ Berkeley',
  url = '',
  license = '',
  long_description= 'Application for the XLab - Mobile research project at UC Berkeley',

  # could also include long_description, download_url, classifiers, etc.
  
)