import setuptools


setuptools.setup(
    name="release-me",
    version="0.1.0",
    author="tadeboro",
    author_email="tadeboro@gmail.com",
    packages=["release_me"],
    license="LICENSE",
    description="Simple Github CLI release helper",
    install_requires=[
        "requests>=2.4.2",
    ],
    entry_points={
        "console_scripts": [
            "github-release = release_me.cli:main",
        ]
    }
)
