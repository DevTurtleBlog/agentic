from setuptools import find_packages, setup

setup(
    name='agentic-py',
    packages=find_packages(include=[
        'agentic', 
        'agentic.a2a',
        'agentic.mcp'
    ]),
    version='0.1.0',
    description='Python framework for implementing multi-agent systems',
    author='devturtleblog@gmail.com',
    install_requires=['uvicorn', 'fastapi', 'a2a-sdk', 'fastapi-mcp'],
    extras_require={
        'dev': ['pytest', 'pytest-runner'],
        'test': ['pytest'],
    },
)