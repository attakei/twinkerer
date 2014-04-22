import os
from setuptools import setup, find_packages
"""setup script
"""

base_dir = os.path.abspath(os.path.dirname(__file__))

requires = [
    'tinkerer',
    'python-twitter',
]
test_requires = [
    'pytest',
]

classifiers = [
    'Programming Language :: Python',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    name='twinkerer',
    version='0.0.1',
    description="tinkerer small extension to use twitter api.",
    author='attakei',
    author_email='attakei@gmail.com',
    url='http://attakei.net/',
    classifiers=classifiers,
    
    install_requires=requires,
    test_requires=test_requires,
    
    packages=find_packages(),
)