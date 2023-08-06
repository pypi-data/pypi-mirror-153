import setuptools
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name="mojtabaahn-pypi-test",
    # version="0.0.4",
    setuptools_git_versioning={
        "enabled": True,
    },
    setup_requires=["setuptools-git-versioning"],
    url="https://github.com/mojtabaahn/pypi-test",
    author="Mojtabaa Habibain",
    author_email="mojtabaa.hn@gmail.com",
    description="Testing Pypi",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)