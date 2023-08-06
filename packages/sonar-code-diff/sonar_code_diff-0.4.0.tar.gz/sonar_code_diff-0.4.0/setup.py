#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Steve Graham",
    author_email='steve@ioka.tech',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Sonar Code Diff is used to run a diff between a test code base and known code base",
    entry_points={
        'console_scripts': [
            'sonar-code-diff=sonar_code_diff.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sonar_code_diff',
    name='sonar_code_diff',
    packages=find_packages(include=['sonar_code_diff', 'sonar_code_diff.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/iokatech/public/sonar_code_diff',
    version='0.4.0',
    zip_safe=False,
)
