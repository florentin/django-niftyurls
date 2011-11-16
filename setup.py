#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup, find_packages

setup(
    name='django-niftyurls',
    version='1.0.0-alpha',
    description='A popurls style Django application.',
    author='Florentin Sardan',
    author_email='florentinwww@gmail.com',
    long_description=open('README.md', 'r').read(),
    url='http://www.betterprogramming.com/',
	packages=find_packages(exclude=('demo_project')),
    packages=[
        'niftyurls',
    ],
	install_requires = [
        'Django>=1.2.1',
        'PIL',
        'feedparser',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
