from setuptools import setup, find_packages

setup(
    name='aos_metadata_collector',
    version='2.0.1',
    author="Jianwei Li",
    author_email="lijianwe@amazon.com",
    description="OpenSearch metadata collector for operational review",
    scripts=['metadata_collector'],
    packages=find_packages(),
    package_data={
        "": ["*.yml"],
    },
    install_requires=[
        "requests",
        "requests-aws4auth",
        "boto3",
        "pyyaml"
    ],
 )