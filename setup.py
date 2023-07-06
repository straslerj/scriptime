from setuptools import setup

setup(
    name="scriptime",
    version="0.0.10",
    author="Jake Strasler",
    author_email="jstr36@gmail.com",
    description="A Python library to notify when a script has finished running and providing insights such as run time, CPU and RAM usage, and more.",
    packages=["scriptime"],
    package_data={"scriptime": ["resources/alert.wav"]},
    install_requires=[
        "psutil",
        "simpleaudio",
    ],
)
