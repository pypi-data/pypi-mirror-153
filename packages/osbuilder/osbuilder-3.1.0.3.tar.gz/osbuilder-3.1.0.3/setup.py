# -*- coding: utf-8
# author: zarhin
# date: 2020/7/21 16:35

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(name='osbuilder',
      version='3.1.0.3',
      description='The pre-& post-processing for openseespy.',
      author='zarhin',
      author_email='lizaixianvip@live.com',
      include_package_data=True,
      install_requires=[
          'numpy>=1.18.1', 'matplotlib>=3.1.3', 'scipy>=1.5.0',
          'openseespy>=3.2.2.6'
      ],
      packages=find_packages(exclude=('tests', 'docs')))
