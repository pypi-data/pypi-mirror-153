from setuptools import setup

setup(
    name='pipelines_test',
    version='0.3.17',
    description='Test Pipelines',
    long_description='Test Pipelines',
    author='Julia Patacz',
    author_email='julia.patacz@gmail.com',
    packages=['pipelines'],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.20.0',
        'makefun>=1.10.0'
    ],
)
