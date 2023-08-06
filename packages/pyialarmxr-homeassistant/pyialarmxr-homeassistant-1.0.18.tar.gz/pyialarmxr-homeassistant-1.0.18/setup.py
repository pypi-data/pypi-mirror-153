"""Setup for aiohue."""
from setuptools import find_packages, setup

setup(
    name="pyialarmxr-homeassistant",
    version="1.0.18",
    license="MIT License",
    url="https://github.com/bigmoby/pyialarmxr",
    author="Fabio Mauro, Ludovico de Nittis",
    author_email="bigmoby.pyialarmxr@gmail.com",
    description="A simple library to interface with iAlarmXR systems, built for use with Home Assistant",
    packages=find_packages(),
    zip_safe=True,
    platforms="any",
    install_requires=["lxml", "xmltodict"],
    python_requires=f">=3.8",
    classifiers=[
      "Development Status :: 4 - Beta",
      "Intended Audience :: Developers",
      "Programming Language :: Python :: 3",
    ],
)
