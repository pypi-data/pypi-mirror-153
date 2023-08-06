# https://docs.pytest.org/en/6.2.x/goodpractices.html

from setuptools import find_packages, setup

setup(
    name='avemedi_lib',
    packages=find_packages(include=['avemedi_lib']),
    version='0.1.0',
    description='This library help in getting a "average value of numbers list" and "get median (for ordered, unordered list of numbers and even or odd list values)". Enjoy.',
    author='zelenchyks@gmail.com',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.1.2'],
    test_suite='tests',
)
