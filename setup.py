from setuptools import setup

setup(
    name="scriptimer",
    version="0.0.1",
    author="Jake Strasler",
    author_email="jstr36@gmail.com",
    description="A Python library to notify when a script has finished running and providing insights such as run time, CPU and RAM usage, and more.",
    packages=["scriptimer"],
    install_requires=[
        "psutil",
        "simpleaudio",
    ],
)