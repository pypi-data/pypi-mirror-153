import subprocess

try:
    import pypandoc

    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


def get_tag():
    tag = subprocess.getoutput('git tag --sort=version:refname | tail -n1')
    commits = subprocess.getoutput(f'git rev-list {tag}..HEAD --count')
    return f'{tag}.{commits}'


import setuptools

setuptools.setup(
    name="algora-sdk",
    version=get_tag(),
    author="Algora Labs",
    author_email="hello@algoralabs.com",
    description="Algora Labs Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.algoralabs.com",
    packages=setuptools.find_packages(exclude=["*.test", "*.test.*", "test.*", "test", "ALGORA_README.md"]),
    package_data={'config': ['config.yml']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
    # TODO: Add version requirements to packages
    install_requires=[
        "pypandoc",
        "pytest",
        "requests",
        "pandas",
        "cachetools",
        "pydash",
        "PyYaml",
        "scipy",
        "pydantic",
        "fastapi",
        "pyarrow",
        "fastparquet",
        "aiohttp",
        "asyncio"
    ]
)
