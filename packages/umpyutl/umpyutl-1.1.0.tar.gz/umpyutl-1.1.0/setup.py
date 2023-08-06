import setuptools

with open("./README.md", "r") as fileobj:
    long_description = fileobj.read()

# Consider appending username to name in order to reduce possible package name collisions.
setuptools.setup(
    name="umpyutl",
    version="1.1.0",
    author="Anthony Whyte",
    author_email="anthwhyte@gmail.com",
    description="Utility classes and functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='arwhyte, utilities, umpyutl',
    url="https://github.com/umsi-arwhyte/umpyutl",
    install_requires=['requests'],
    packages=setuptools.find_packages(include=['umpyutl', 'umpyutl.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
