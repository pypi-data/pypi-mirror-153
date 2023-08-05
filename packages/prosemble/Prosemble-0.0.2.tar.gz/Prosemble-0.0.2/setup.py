import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Prosemble",
    version="0.0.2",
    author="Nana Abeka Otoo",
    author_email="abekaotoo@gmail.com",
    description="Prototype based ensemble classifier",
    url="https://github.com/naotoo1/prosemble",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['ensemble', 'Prototype ensemble'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    py_modules=["prosemble"],
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'scikit-learn',
        'scipy'

    ]
)
