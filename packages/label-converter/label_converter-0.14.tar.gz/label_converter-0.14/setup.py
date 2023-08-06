import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='label_converter',
    version='0.14',
    author="Miika Launiainen",
    author_email="miika.launiainen@fns.fi",
    description="HTML to label png converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/finnishnetsolutions/label-converter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
