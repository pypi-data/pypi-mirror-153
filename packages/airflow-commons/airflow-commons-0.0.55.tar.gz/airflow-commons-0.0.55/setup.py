import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airflow-commons",
    version="0.0.55",
    author="Startup Heroes",
    description="Common functions for airflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/migroscomtr/airflow-commons/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pytz>=2018.4",
        "datetime",
        "google-cloud-bigquery==2.34.3",
        "pandas",
        "sqlalchemy",
        "pymysql",
        "boto3==1.19.8",
        "botocore==1.22.8",
        "aiobotocore==2.0.1",
        "pyyaml",
        "s3fs==2021.11.1",
        "s3transfer",
        "pyarrow>=5.0.0",
    ],
    include_package_data=True,
)
