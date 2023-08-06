try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup
import sys

extra = {}
# if sys.version_info >= (3, ):
#    extra['use_2to3'] = True

setup(
    name='PyCST',
    packages=['pycst', ],
    version='0.0.1',
    author='William Yates',
    author_email='william.yates4@gmail.com',
    url='https://github.com/Yates1011/PyCST',
    description='Python interface to the CST',
    long_description='''
    PyCST''',
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Natural Language :: English',
                 'Intended Audience :: Developers',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python'],
    install_requires=['requests'],
    **extra
    )
