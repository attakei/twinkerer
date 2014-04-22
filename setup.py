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

entry_points = {
    'console_scripts': [
        'twinker = twinkerer:main',
    ],
}


with open(os.path.join(base_dir, 'README.rst')) as f:
    readme = f.read()


setup(
    name='twinkerer',
    version='0.0.1',
    description="tinkerer small extension to use twitter api.",
    long_description=readme,
    author='attakei',
    author_email='attakei@gmail.com',
    license='MIT License',
    url='http://attakei.net/',
    classifiers=classifiers,
    
    install_requires=requires,
    test_requires=test_requires,
    
    packages=find_packages(),
    entry_points=entry_points,
)