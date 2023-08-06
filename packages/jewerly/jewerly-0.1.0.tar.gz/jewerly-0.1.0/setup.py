import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
def _requires_from_file(filename):
    return open(filename, encoding="utf8").read().splitlines()

def _get_version(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    version = None
    for line in lines:
        if "__version__" in line:
            version = line.split()[2]
            break
    return version.replace('"', '')

setuptools.setup(
    name="jewerly",
    version=_get_version("jewerly/__init__.py"),
    author="DMS",
    author_email="masato190411@gmail.com",
    description="This can easy to use discord-api.py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/discord-api-py-org/jewerly",
    install_requires=_requires_from_file('requirements.txt'),
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
