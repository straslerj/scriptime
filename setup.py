from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="scriptime",
    version="0.1.6",
    author="Jake Strasler",
    author_email="jstr36@gmail.com",
    description="A Python library to notify when a script has finished running and providing insights such as run time, CPU and RAM usage, and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["scriptime"],
    package_data={"scriptime": ["scriptime/alert.wav"]},
    include_package_data=True,
    install_requires=["psutil", "simpleaudio", "setuptools"],
)
