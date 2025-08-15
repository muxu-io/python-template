"""Setup configuration for hello-mqtt package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hello-mqtt",
    version="0.1.0",
    author="Template User",
    author_email="user@example.com",
    description="A simple MQTT hello world package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/user/hello-mqtt",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "paho-mqtt>=1.6.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "ruff>=0.1.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "bandit[toml]>=1.7.0",
            "pip-audit>=2.6.0",
        ],
    },
)