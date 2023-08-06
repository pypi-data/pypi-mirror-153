from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="async_pycatbox",
    version="1.0",
    py_modules=find_packages(),
    author="Andrew McGrail",
    author_email="andrewjerrismcgrail@gmail.com",
    license="Apache License, Version 2.0, see LICENSE file",
    description="Async version of pycatbox, a Python API wrapper for catbox.moe.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["aiohttp"],
    packages=["async_pycatbox"],
)
