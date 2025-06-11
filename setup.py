from setuptools import find_packages, setup

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='agentic-a2a',
    packages=find_packages(include=[
        'agentic', 
        'agentic.a2a',
        'agentic.mcp'
    ]),
    version='0.1.6',
    description='Python framework for implementing multi-agent systems',
    author='devturtleblog@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DevTurtleBlog/agentic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=['uvicorn', 'fastapi', 'a2a-sdk', 'fastapi-mcp'],
    extras_require={
        'dev': ['pytest', 'pytest-runner'],
        'test': ['pytest'],
    },
)