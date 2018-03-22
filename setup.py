import re
import os
import sys
import shutil

from setuptools import setup
from setuptools import find_packages


def get_version() -> str:
  """Helper function to fetch the package version from the package __init__.py file"""
  base_dir = os.path.dirname(os.path.abspath(__file__))
  with open(os.path.join(base_dir, 'luno/__init__.py'), 'r') as f:
    content = f.read()

  rpattern = re.compile("__version__\\s+=\\s+'?(?P<package_version>[.\\d]+)'?")
  package_version = (
      rpattern
        .match(content)
        .groupdict()['package_version']
      )

  return package_version


def get_readme():
  with open('README.md') as f:
    return f.read()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('luno.egg-info')
    sys.exit()


if __name__ == '__main__':
    version = get_version()
    readme = get_readme()

    setup(
      name='luno',
      version=version,
      author='Bradley Stuart Kirton',
      author_email='bradleykirton@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      description='Luno Crypto Currency Exchanage Python API',
      long_description=readme,
      long_description_content_type='text/markdown',
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
      install_requires=['requests'],
      extras_require={'dev': ['pytest', 'requests-mock', 'pypandoc', 'wheel', 'twine'], 'async': ['treq']}
    )