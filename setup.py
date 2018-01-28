import re
import os

from setuptools import setup
from setuptools import find_packages

# Some helper functions
def get_version():
  PATTERN = "__version__\s+=\s+'(?P<version>.*)'"

  with open('luno/__init__.py', 'r') as f:
      match = re.search(PATTERN, f.read())
      match_dict = match.groupdict()

  return match_dict['version']


requirements = [
    'requests'
]


if __name__ == '__main__':
    version = get_version()

    setup(
      name='luno',
      version=version,
      author='Bradley Stuart Kirton',
      author_email='bradleykirton@gmail.com',
      packages=find_packages(),
      description='Luno Crypto Currency Exchanage Python API',
      url='https://github.com/BradleyKirton/luno',
      license='MIT',
      keywords=['exchange', 'crypto currency', 'rest', 'api', 'bitcoin', 'etherium'],
      classifiers=[
         'Development Status :: 4 - Beta',
         'Intended Audience :: Developers',
         'Intended Audience :: Financial and Insurance Industry',
         'Operating System :: OS Independent',
         'Topic :: Office/Business :: Financial :: Investment',
         'Topic :: Software Development :: Libraries :: Python Modules',
         'License :: OSI Approved :: MIT License',
         'Programming Language :: Python :: 3 :: Only'
      ],
      install_requires=requirements,
      extras_require={'dev': ['pytest', 'requests-mock'], 'async': ['treq']}
    )