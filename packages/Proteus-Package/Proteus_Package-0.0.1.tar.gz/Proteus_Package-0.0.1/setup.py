import setuptools

setuptools.setup(
    name="Proteus_Package",
    version="0.0.1",
    author="Proteustech PVT. LTD.",
    author_email="aniket.gadge@proteustech.in",
    description="Proteustech Files",
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    python_requires=">=3.6",
)
