import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "toumoro_cdk.cognito",
    "version": "1.0.4",
    "description": "Creates a cognito userpool and app client",
    "license": "Apache-2.0",
    "url": "https://github.com/toumoro/toumoro-cdk.git",
    "long_description_content_type": "text/markdown",
    "author": "Your name<Your email address>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/toumoro/toumoro-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "toumoro_cdk.cognito",
        "toumoro_cdk.cognito._jsii"
    ],
    "package_data": {
        "toumoro_cdk.cognito._jsii": [
            "cognito@1.0.4.jsii.tgz"
        ],
        "toumoro_cdk.cognito": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.25.0, <3.0.0",
        "constructs>=10.1.22, <11.0.0",
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
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
