"""
BetaRoot Setup Configuration
الإعداد النهائي لتثبيت المكتبة
"""

from setuptools import setup, find_packages
from pathlib import Path

# قراءة الـ README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="betaroot-ai",
    version="0.1.0-alpha",
    author="Meflahi Abdelkader",
    author_email="contact@betaroot.dev",
    description="BetaRoot - إطار ذكاء اصطناعي رمزي قائم على المنطق الآحادي والسببية الحقيقية",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/betaroot/betaroot-ai",
    project_urls={
        "Bug Tracker": "https://github.com/betaroot/betaroot-ai/issues",
        "Documentation": "https://betaroot.readthedocs.io",
        "Source Code": "https://github.com/betaroot/betaroot-ai",
    },
    packages=find_packages(include=["betaroot", "betaroot.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: Arabic",
        "Natural Language :: English",
    ],
    python_requires=">=3.11",
    install_requires=[
        "numpy>=1.24.0",
        "networkx>=3.0",
        "pydantic>=2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "isort>=5.12",
        ],
        "viz": [
            "matplotlib>=3.7.0",
            "plotly>=5.13",
        ],
    },
    entry_points={
        "console_scripts": [
            "betaroot=betaroot.cli:main",   # سنضيفه لاحقاً
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "ai", "artificial-intelligence", "symbolic-ai", "causal-reasoning",
        "explainable-ai", "unary-logic", "betaroot", "one-solution"
    ],
)
