#!/usr/bin/env python3
"""
JsonSchemaCodeGen - Setup Configuration

Copyright © 2025-2030, All Rights Reserved
Ashutosh Sinha
Email: ajsinha@gmail.com

LEGAL NOTICE:
This software is proprietary and confidential. Unauthorized copying,
distribution, modification, or use is strictly prohibited without
explicit written permission from the copyright holder.

Patent Pending: Certain implementations may be subject to patent applications.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="jsonschemacodegen",
    version="1.0.0",
    author="Ashutosh Sinha",
    author_email="ajsinha@gmail.com",
    description="Commercial Grade JSON Schema to Python Code Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajsinha/jsonschemacodegen",
    license="Proprietary",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "faker": ["faker>=18.0.0"],
        "requests": ["requests>=2.28.0"],
        "jsonschema": ["jsonschema>=4.17.0"],
        "pydantic": ["pydantic>=2.0.0"],
        "all": [
            "faker>=18.0.0",
            "requests>=2.28.0",
            "jsonschema>=4.17.0",
            "pydantic>=2.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "jsonschemacodegen=jsonschemacodegen.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "jsonschemacodegen": ["py.typed"],
    },
    zip_safe=False,
    keywords=[
        "json-schema",
        "code-generator",
        "pydantic",
        "dataclass",
        "validation",
        "schema",
        "python",
        "typing",
    ],
    project_urls={
        "Documentation": "https://github.com/ajsinha/jsonschemacodegen#readme",
        "Source": "https://github.com/ajsinha/jsonschemacodegen",
        "Issues": "https://github.com/ajsinha/jsonschemacodegen/issues",
    },
)
