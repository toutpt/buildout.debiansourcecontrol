from setuptools import setup, find_packages
import os

version = '1.0'

setup(
    name='buildout.debiansourcecontrol',
    version=version,
    description="Buildout extension to generate a debian source control file .dsc",
    long_description=open("README.rst").read() + "\n" +
                     open("CHANGES.txt").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
      "Environment :: Web Environment",
      "License :: OSI Approved :: GNU General Public License (GPL)",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Python :: 2.7",
    ],
    keywords='plone',
    author='JeanMichel aka toutpt',
    author_email='toutpt@gmail.com',
    url='https://github.com/toutpt/buildout.debiansourcecontrol',
    license='gpl',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['buildout'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
    entry_points = { 
        "zc.buildout.extension": ["default = buildout.debiansourcecontrol:start"],
        "zc.buildout.unloadextension": ["default = buildout.debiansourcecontrol:finish"],
    },
)
