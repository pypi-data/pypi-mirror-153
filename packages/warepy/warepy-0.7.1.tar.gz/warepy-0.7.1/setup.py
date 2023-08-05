from setuptools import setup, find_packages

from warepy import __version__ as version


with open("requirements.txt", "r") as file:
    install_requires = [x.strip() for x in file.readlines()]

setup(
    name="warepy",
    packages=find_packages(),
    include_package_data=True,
    version=version,
    license="MIT",
    description="My toolkit for Python.",
    author="Alexander Ryzhov",
    author_email="thed4rkof@gmail.com",
    url="https://github.com/ryzhovalex/warepy",
    keywords=["toolkit", "python-core"],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",

        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.10",
    ],
)
