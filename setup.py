from setuptools import setup, find_packages

NAME = 'pythoms'
VERSION = '1.0.2.1'
AUTHOR = 'Lars Yunker'

PACKAGES = find_packages()
KEYWORDS = ', '.join([
    'mass spectrometry',
    'mass spec',
    'mzML',
    'isotope pattern',
    'HUPO PSI-MS',
])

with open('README.MD') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description='A Python library to aid in the processing and interpretation of mass spectrometric data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    url='https://github.com/larsyunker/PythoMS',
    packages=PACKAGES,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Operating System :: OS Independent',
        'Natural Language :: English'
    ],
    keywords=KEYWORDS,
)
