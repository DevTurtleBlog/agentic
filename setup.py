from setuptools import find_packages, setup

setup(
    name='agentic',
    packages=find_packages(include=['agentic']),
    version='0.1.0',
    description='Python framework for implementing multi-agent systems',
    author='gderito90@gmaill.com',
    install_requires=['uvicorn', 'fastapi', 'a2a-sdk'],
    extras_require={
        'dev': ['pytest', 'pytest-runner'],
        'test': ['pytest'],
    },
)