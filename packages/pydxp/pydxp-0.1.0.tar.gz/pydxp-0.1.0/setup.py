import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydxp",
    version="0.1.0",
    author="wisetux",
    author_email="prasadkumar013@gmail.com",
    url="https://gitlab.com/wisetux/pydxp",
    description="Python module for Nectar DXP",
    long_description="pydxp is a Python wrapper around the Nectar DXP dashboard REST API",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    py_modules=["pydxp"],
    package_dir={'pydxp': 'src'},  # Directory of the source code of the package
    install_requires=[
        'requests',
        'json',
    ]
)
