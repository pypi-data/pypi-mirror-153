from setuptools import find_packages, setup

setup(
    name='PyHyperChat',
    packages=find_packages(include=['PyHyperChat']),
    version='0.1.5',
    description='HyperChat Bot Library',
    author='ConnorDev',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner', 'requests', 'coloredlogs'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
