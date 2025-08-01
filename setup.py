import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytcp_dict_messanger",
    version="0.1.0",
    author="Aleksandr Chansyk",
    author_email="alexandr.chansyk@gmail.com",
    description="TCP messanger that allow to send and receive dictionary ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ami3go/pyTCP_dict_messanger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)