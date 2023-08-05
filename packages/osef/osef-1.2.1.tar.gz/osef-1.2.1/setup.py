"""To easily install project."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="osef",
    setuptools_git_versioning={
        "enabled": True,
    },
    setup_requires=["setuptools-git-versioning"],
    packages=find_packages(exclude=["tests"]),
    author="Outsight Developers",
    author_email="support@outsight.tech",
    description="Osef file/stream tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["numpy>=1.15.4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
