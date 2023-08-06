import io
from pathlib import Path
from setuptools import setup, find_packages

# The directory containing this file
DIRECTORY = Path(__file__).parent

# The text of the README file
README = (DIRECTORY / "README.md").read_text()

# Automatically capture required modules in requirements.txt for install_requires
with io.open(DIRECTORY / "requirements.txt", encoding="utf-8") as f:
    requirements = f.read().split("\n")

install_requires = [
    r.strip()
    for r in requirements
    if not ("git+" in r or r.startswith("#") or r.startswith("-"))
]

# Configure dependency links
dependency_links = [
    r.strip().replace("git+", "") for r in requirements if "git+" not in r
]


setup(
    name="cli_plot",
    description="A commandline app for plotting datafiles",
    version="1.1.1",
    # version="1.0.post7",
    packages=["cli_plot"],
    install_requires=install_requires,
    python_requires=">=3.6",
    entry_points="""
        [console_scripts]
        cli_plot=cli_plot.plot:main
    """,  # Create a script plot that call main() in within plot/plot.py
    author="John Lee Cooper",
    keyword="plot, matplotlib, cli",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/John-Lee-Cooper/cli_plot",
    download_url="https://github.com/John-Lee-Cooper/cli_plot/archive/1.0.0.tar.gz",
    dependency_links=dependency_links,
    author_email="cooperjl90@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)