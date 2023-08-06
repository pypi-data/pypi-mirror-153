"""
The setup file for the Voice_Helper package
"""

# import what we need

import os
from setuptools import setup, find_packages

# set the version and descriptions

VERSION = "0.2"
DESCRIPTION = "Custom virtual assistant"
LONG_DESCRIPTION = "Create your own virtual assistant"

# set up the file

setup(
    name="voice_helper",
    version=VERSION,
    author="Eli Tremoulet",
    author_email="<eliharvey007@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pyttsx3", "SpeechRecognition"],
    keywords=["virtual assistant", "voice assistant"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
