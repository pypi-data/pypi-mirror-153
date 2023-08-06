import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twitter_2_album",
    version="0.0.25",
    author="Yunzhi Gao",
    author_email="gaoyunzhi@gmail.com",
    description="Return photo list and caption (markdown format) from twitter.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaoyunzhi/twitter_2_album",
    packages=setuptools.find_packages(),
    package_data={'twitter_2_album': ['allowlist']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyyaml',
        'telegram_util',
        'tweepy'
    ],
    python_requires='>=3.0',
)