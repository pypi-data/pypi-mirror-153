#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='make-up-tools',
      version='0.0.11',
      description='just for job',
      long_description=open('README.md', 'r').read(),
      long_description_content_type="text/markdown",
      author='NA',
      author_email='martinlord@foxmail.com',
      url='https://gitee.com/mahaoyang/make_up',
      packages=find_packages(
          include=[
              'make_up_tools*',
          ]
      ),
      package_data={
          '': ['*.txt'],
      },
      include_package_data=True,
      license='LICENSE.txt',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3 :: Only",
          'Topic :: Software Development :: Libraries'
      ],
      )
