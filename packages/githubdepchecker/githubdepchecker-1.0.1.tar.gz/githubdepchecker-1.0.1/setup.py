
from setuptools import setup, find_packages

from codecs import open
from distutils.util import convert_path
from os import path

here = path.abspath(path.dirname(__file__))

short_description = (
    "CLI Tool to check the dependencies of github repositories and create a pull request if packages need to get updated.")


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='githubdepchecker',
    version="1.0.1",

    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/dyte-submissions/dyte-vit-2022-Shubh0405',

    author='Shubh Gupta',
    author_email='shubhngupta04@gmail.com',

    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Shells',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],

    packages=find_packages(exclude=['tests', 'tests.*']),

    # What does your project relate to?
    keywords='github,pull-requests,npm,npm-packages,cli-tool',

    python_requires='>=3.7',
    
    
    install_requires=['requests'],

   
    extras_require={
        'dev': [
            'setuptools',
            'twine',
            'wheel'
        ]
    },

   
    package_data={
        'githubdepchecker': ['config.json']
    },

    
    entry_points={
        'console_scripts': [
            'githubdepchecker=githubdepchecker.githubdepchecker:main'
        ]
    },
)