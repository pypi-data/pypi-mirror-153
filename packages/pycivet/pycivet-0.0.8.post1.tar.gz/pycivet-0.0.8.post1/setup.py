from setuptools import setup, find_packages
import os
import shutil
import glob

if 'CI' not in os.environ and not shutil.which('adapt_object_mesh'):
    raise Exception(
        'CIVET binaries such as "adapt_object_mesh" not found in $PATH.'
        '\nHint: consider using container images, such as '
        '"docker.io/fnndsc/mni-conda-base:civet2.1.1-python3.10.2"'
    )

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='pycivet',
    version='0.0.8.post1',
    description='Object-oriented CIVET bindings for Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Jennings Zhang',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pycivet',
    project_urls={
        'Documentation': 'https://fnndsc.github.io/pycivet/',
        'Source': 'https://github.com/FNNDSC/pycivet',
        'Tracker': 'https://github.com/FNNDSC/pycivet/issues',
    },
    license='MIT',
    packages=find_packages(exclude=('*.tests',)),
    python_requires='>=3.10.2',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    package_data={
        'civet.extraction.kernels': ['data/*']
    },
    scripts=glob.glob('scripts/*')
)
