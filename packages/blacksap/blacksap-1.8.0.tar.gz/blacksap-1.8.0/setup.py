# coding=utf-8
"""Setup script for blacksap project"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='blacksap',
      version='1.8.0',
      author='Jesse Almanrode',
      author_email='jesse@almanrode.com',
      description='Track torrent RSS feeds',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://bitbucket.org/isaiah1112/blacksap',
      license='GNU General Public License v3 or later (GPLv3+)',
      py_modules=['blacksap'],
      python_requires='>3.7',
      install_requires=['click>=8.1.3',
                        'colorama>=0.4.4',
                        'feedparser>=6.0.10',
                        'PySocks>=1.7.1',
                        'requests>=2.27.1',
                        ],
      platforms=['Linux', 'Darwin'],
      entry_points={
          'console_scripts': [
              'blacksap = blacksap:cli',
          ]
      },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Communications :: File Sharing',
          'Topic :: Utilities',
          ],
      )
