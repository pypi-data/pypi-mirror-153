import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-valheim",
    "version": "0.0.23",
    "description": "cdk-valheim",
    "license": "Apache-2.0",
    "url": "https://github.com/gotodeploy/cdk-valheim.git",
    "long_description_content_type": "text/markdown",
    "author": "gotodeploy<1491134+gotodeploy@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/gotodeploy/cdk-valheim.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_valheim",
        "cdk_valheim._jsii"
    ],
    "package_data": {
        "cdk_valheim._jsii": [
            "cdk-valheim@0.0.23.jsii.tgz"
        ],
        "cdk_valheim": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.15.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.59.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
