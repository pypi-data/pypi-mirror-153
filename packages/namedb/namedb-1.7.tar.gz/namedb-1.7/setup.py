from setuptools import setup, find_packages
import codecs, os

VERSION = '1.7'
DESCRIPTION = 'An easy to use, fast and open source document based python database'

setup(
  name = 'namedb',
  version = VERSION,
  author = "Name",
  author_email = "not_name47@protonmail.com",
  install_requires=[],
  keywords = ['python', 'database', 'fast', 'document', 'futuristic'],
  classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2',
    'Natural Language :: English',
    'Operating System :: OS Independent'
  ],
  license='GNU General Public License v2.0',
  long_description=open('readme.md', 'r').read(),
  long_description_content_type='text/markdown'
)