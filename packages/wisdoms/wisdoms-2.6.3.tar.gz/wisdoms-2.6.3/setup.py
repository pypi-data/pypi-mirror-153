# Created by Q-ays.
# whosqays@gmail.com


import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="wisdoms",
    version="2.6.3",
    author="tzxd group",
    author_email="whosqays@qq.com",
    description="fix dapr invoke function",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/soft-project/wisdom-lib",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyYaml'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
