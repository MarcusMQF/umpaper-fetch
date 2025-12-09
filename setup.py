#!/usr/bin/env python3
"""
Setup script for umpaper-fetch package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
try:
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    requirements = [
        'selenium>=4.15.2',
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.2',
        'webdriver-manager>=4.0.1',
        'lxml>=4.9.3',
        'urllib3>=2.0.7',
        'certifi>=2023.7.22',
        'tqdm>=4.66.1'
    ]

setup(
    name="umpaper-fetch",
    version="1.0.7",
    author="Marcus Mah",  # Replace with your actual name
    author_email="marcusmah6969@gmail.com",
    description="Automated downloader for University Malaya past year exam papers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarcusMQF/umpaper-fetch",  # Replace with your repo URL
    project_urls={
        "Bug Reports": "https://github.com/MarcusMQF/umpaper-fetch/issues",
        "Source": "https://github.com/MarcusMQF/umpaper-fetch",
        "Documentation": "https://github.com/MarcusMQF/umpaper-fetch#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "umpaper=umpaper_fetch.cli:main",
        ],
    },
    keywords="university malaya um exam papers downloader automation selenium",
    include_package_data=True,
    package_data={
        "umpaper_fetch": ["*.md", "*.txt"],
    },
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=1.0",
        ],
    },
    zip_safe=False,
) 