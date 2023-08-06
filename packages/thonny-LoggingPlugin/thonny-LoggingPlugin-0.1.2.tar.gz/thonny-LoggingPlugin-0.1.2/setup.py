import setuptools
import os.path

setupdir = os.path.dirname(__file__)

REQUIREMENTS = ["thonny>=3.3.13"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thonny-LoggingPlugin",
    version="0.1.2",
    author="Corentin",
    author_email="corentin.duvivier.etu@univ-lille.fr",
    description="A plugin that logs and send all the user's actions to an LRS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.univ-lille.fr/corentin.duvivier.etu/thonny-plugin-journalisation",
    project_urls={
    },
    platforms=["Windows", "macOS", "Linux"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "thonnycontrib": ["*.py"],
        "thonnycontrib.thonny_LoggingPlugin": ["*.py"],
        "thonnycontrib.thonny_LoggingPlugin.utils": ["*.py"],
    },
    packages=["thonnycontrib","thonnycontrib.thonny_LoggingPlugin","thonnycontrib.thonny_LoggingPlugin.utils"],
    install_requires=REQUIREMENTS,
    python_requires=">=3.6",
)