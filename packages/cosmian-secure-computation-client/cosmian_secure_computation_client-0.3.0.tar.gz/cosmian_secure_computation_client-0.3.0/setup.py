"""setup module."""

from pathlib import Path

from setuptools import setup, find_packages

setup(
    name="cosmian_secure_computation_client",
    version="0.3.0",
    url="https://cosmian.com",
    license="MIT",
    author="Cosmian Tech",
    author_email="tech@cosmian.com",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8.0",
    description="Python client library for Cosmian Secure Computation",
    packages=find_packages(),
    zip_safe=True,
    install_requires=[
        "requests>=2.27.0,<3.0.0",
        "pynacl>=1.5.0,<1.6.0",
        "cryptography>=36.0.2,<37.0.0",
        "pyjwt>=2.3.0,<2.4.0"
    ],
    test_requires=[
        "pytest>=7.0.1,<8.0.0"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)
