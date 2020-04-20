import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xmu",
    version="0.1.0",
    author="Georgiy Kozlov",
    author_email="appendix.y.z@gmail.com",
    description="eXtensible MarkUp parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/decorator-factory/xmu-python",
    packages=["xmu", "xmu.extensions"],
    install_requires=[
        "attrdict",
        "lark-parser",
        "libsass",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
