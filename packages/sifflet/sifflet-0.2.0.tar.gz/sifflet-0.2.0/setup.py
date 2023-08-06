import setuptools

import sifflet

long_description = open("README.md", "r", encoding="utf-8").read()
requirements = [i.strip() for i in open("requirements.txt").readlines()]

setuptools.setup(
    name="sifflet",
    version=sifflet.__version__,
    author="Sifflet",
    author_email="support@siffletdata.com",
    description="Sifflet sdk",
    py_modules=["sifflet"],
    entry_points={
        "console_scripts": [
            "sifflet = sifflet.cli:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(include=["sifflet", "sifflet.*"]),
    python_requires=">3.6",
    # extras_require={
    #     'airflow': [],
    # }
    install_requires=requirements,
)
