import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="MtySdk",
    version="0.1.3",
    author="Credi He",
    author_email="17316365004@sina.cn",
    description="This is a demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/hexingchi/mty-sdk.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)