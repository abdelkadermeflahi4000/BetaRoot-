"""
BetaRoot Setup Configuration

This script configures the installation of the BetaRoot AI Framework.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="betaroot-ai",
    version="0.1.0a1",  # Alpha version
    author="BetaRoot Contributors",
    author_email="contact@betaroot.dev",
    description="A symbolic AI framework based on unary logic and causal reasoning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/betaroot/betaroot-ai",
    project_urls={
        "Bug Tracker": "https://github.com/betaroot/betaroot-ai/issues",
        "Documentation": "https://betaroot.readthedocs.io",
        "Source Code": "https://github.com/betaroot/betaroot-ai",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "sympy>=1.12",
        "networkx>=3.0",
        "pydantic>=2.0",
        "pydantic-core>=2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "hypothesis>=6.70",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "isort>=5.12",
            "sphinx>=6.0",
            "sphinx-rtd-theme>=1.2",
        ],
        "viz": [
            "matplotlib>=3.7.0",
            "plotly>=5.13",
        ],
        "blockchain": [
            "web3>=6.0",
            "bitcoinlib>=0.6",
        ],
        "notebook": [
            "jupyter>=1.0",
            "notebook>=6.5",
            "ipython>=8.10",
        ],
    },
    entry_points={
        "console_scripts": [
            "betaroot=betaroot.cli:main",
        ],
    },
    include_package_data=True,
    keywords=[
        "ai",
        "artificial-intelligence",
        "machine-learning",
        "unary-logic",
        "symbolic-reasoning",
        "causal-reasoning",
        "explainability",
        "interpretability",
        "blockchain",
        "bitcoin",
    ],
    zip_safe=False,
)
