#!/usr/bin/env python

from distutils.core import setup

setup(name='make-up-tools',
      version='0.0.1',
      description='just for job',
      long_description=open('README.md', 'r').read(),
      long_description_content_type="text/markdown",
      author='NA',
      author_email='martinlord@foxmail.com',
      url='https://gitee.com/mahaoyang/make_up',
      packages=['make_up_tools'],
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
