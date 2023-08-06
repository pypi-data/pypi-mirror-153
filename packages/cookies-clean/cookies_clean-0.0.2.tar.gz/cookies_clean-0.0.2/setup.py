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
  description='Package created to clean your code up!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='http://cookiesservices.xyz/',
  author='CookiesKush420',
  author_email='callumgm20052005@gmail.com',
  license='MIT',
  keywords=['CleanConsole', 'printslow', 'getheaders', 'proxyscrape'], 
  install_requires=['requests', 'colorama'], 
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
  ]
)
