import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kffmpeg",
    version="0.2.46",
    author="Kovacs Kristof-Attila",
    description="kffmpeg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/kffmpeg",
    packages=setuptools.find_packages(),
    install_requires=[
        'kcu>=0.0.73',
        'setuptools>=62.2.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)