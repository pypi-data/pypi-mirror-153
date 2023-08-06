import os, re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

NAME = "cookies_clean"

def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as fp:
        return fp.read()

def _get_version_match(content):
    # Search for lines of the form: # __version__ = 'ver'
    regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_match = re.search(regex, content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def get_version(path):
    return _get_version_match(read_file(path))

setup(
  name=NAME,
  packages=[NAME],
  version=get_version(os.path.join(NAME, '__init__.py')),
  description='Short desc',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='http://cookiesservices.xyz/',
  author='',
  author_email='',
  license='MIT',
  keywords=['Template', 'Template', 'Template'], 
  install_requires=['requests', 'colorama'], # Add any needed packages here that your package will need to work
  # see classifiers https://pypi.org/pypi?%3Aaction=list_classifiers
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
  ]
)
