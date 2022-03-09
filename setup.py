import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="bad-gitlab-sync",
    version="0.1.0",
    author="Zed Tan",
    author_email="zed@shootbird.work",
    description="""Retrieve one or more files from
    a given repository using the GitLab files API.
    Useful when you want to pull a small subset of files
    from a repository without managing git submodules or
    similar.""",
    url="https://github.com/zeddee/bad-gitlab-sync",
    project_urls={
        "Bug Tracker": "https://github.com/zeddee/bad-gitlab-sync/issues",
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0 License",
        "Private :: Do Not Upload",
        ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "python-dotenv~=0.19",
        "python-gitlab~=3.1",
        "requests~=2.27",
        "marshmallow~=3.14",
    ],
    entry_points={
        "console_scripts": [
            "gitlab-filesync=bad-gitlab-filesync:main"
        ]
    }
)
