# coding=utf-8
"""
samgenericservices

py setup.py sdist bdist_wheel
twine upload --config-file D:/twine-config-pypi.pypirc dist/*0.9.2*
"""

from setuptools import setup

setup(name='samgenericservices',
      version='0.9.2',
      packages=['samgenericservices'],
      url='https://t.me/samthesuperhero',
      license='Creative Commons Attribution 4.0 International',
      author='Pavel A. Fomin',
      author_email='fomin-p@yandex.ru',
      description='Classes and functions to use for development of intregration software',
      install_requires=['aiohttp>=3.8.1',
                        'aio_pika>=8.0.3',
                        'aiormq>=6.3.3',
                        'asyncpg>=0.25.0',
                        'boto3>=1.22.8',
                        'botocore>=1.25.8',
                        'bs4>=0.0.1',
                        'multidict>=6.0.2',
                        'viledatools>=1.0.30'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Other Environment',
                   'License :: Other/Proprietary License',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.9',
                   'Topic :: Utilities'],
      zip_safe=False,
      python_requires='>=3.9'
      )
