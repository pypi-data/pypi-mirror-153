from distutils.core import setup

setup(
    # Application name:
    name="Weather rest library",

    # Version number (initial):
    version="1.0.2",

    # Application author details:
    author="Mateusz Urbańczyk",
    author_email="name@addr.ess",

    # Packages
    packages=["rest_requests","steering"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://git.e-science.pl/murbanczyk_252808/murbanczyk252808_dpp_python_pip",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "requests"
    ],
)