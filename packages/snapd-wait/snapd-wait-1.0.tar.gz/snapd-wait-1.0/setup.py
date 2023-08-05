""" Package setup """
import setuptools

PACKAGE = "snapd-wait"


def get_long_description():
    """
    Return long description from `README.md`.
    """
    with open("README.md", "r", encoding="utf-8") as fp:
        return fp.read()


setuptools.setup(
    name=PACKAGE,
    version="1.0",
    author="Matthew R Laue",
    author_email="matt@mindspun.com",
    description="Wait for snapd autorefresh to complete",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=[],
    python_requires=">=3.5",
    install_requires=[],
    extras_require={
        "dev": [
            "flake8",
            "flake8-quotes",
            "freezegun",
            "pylint",
            "pytest",
            "pytest-cov",
            "pytest-mock"
        ]
    },
    scripts=["bin/snapd-wait"]
)
