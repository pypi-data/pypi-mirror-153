import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-aws-iotfleetwise",
    "version": "0.0.0",
    "description": "L2 CDK construct to provision AWS IoT Fleetwise",
    "license": "MIT-0",
    "url": "https://github.com/aws-samples/cdk-aws-iotfleetwise.git",
    "long_description_content_type": "text/markdown",
    "author": "Francesco Salamida<salamida@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws-samples/cdk-aws-iotfleetwise.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_aws_iotfleetwise",
        "cdk_aws_iotfleetwise._jsii"
    ],
    "package_data": {
        "cdk_aws_iotfleetwise._jsii": [
            "cdk-aws-iotfleetwise@0.0.0.jsii.tgz"
        ],
        "cdk_aws_iotfleetwise": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.26.0, <3.0.0",
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
