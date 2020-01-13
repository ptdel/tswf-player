import os
from setuptools import setup, find_packages

cwd = os.path.abspath(os.path.dirname(__file__))

requires = [
    "pyaudio",
    "python-librtmp",
    "ffmpeg",
    "bottle",
    "boddle",
    "pyxattr",
]

setup(
    name="tswf",
    description="listen to tasty shapes with your mates.",
    classifiers=[
        "Development Status :: Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: ffmpeg",
        "Intended Audience :: Internet People",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Internet :: Www/HTTP :: WSGI :: Application",
    ],
    author="@ptdel",
    url="https://github.com/ptdel",
    keywords="flask youtube-dl irc jorny",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="player",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=requires,
)
