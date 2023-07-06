from setuptools import setup

setup(
    name="scriptime",
    version="0.0.18",
    author="Jake Strasler",
    author_email="jstr36@gmail.com",
    description="A Python library to notify when a script has finished running and providing insights such as run time, CPU and RAM usage, and more.",
    packages=["scriptime"],
    package_data={"scriptime": ["scriptime/alert.wav"]},
    include_package_data=True,
    install_requires=[
        "psutil",
        "simpleaudio",
    ],
)
