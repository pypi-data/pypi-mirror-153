import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="listoapi",
    version="0.1.74",
    author="Hugo Villegas <hugo.villegas@listo.mx>",
    author_email="hugo.villegas@listo.mx",
    keywords='api listo listoapi sdk integration python',
    description="Listo SDK module for web API integration",
    long_description=long_description,
    url="https://github.com/listomx/listoapi",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.19.1",
        "pyopenssl==17.5.0",
    ],
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Freely Distributable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
