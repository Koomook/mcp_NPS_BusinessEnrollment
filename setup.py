"""Setup script for backward compatibility with older pip versions."""

from setuptools import setup

# Read the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
)