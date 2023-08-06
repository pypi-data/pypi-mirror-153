import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


INSTALL_REQUIRES = [
    "marshmallow==3.15.0",
    "PyMySQL==1.0.2",
    "python-dateutil==2.8.2",
    "pytz==2022.1",
    "SQLAlchemy==1.4.35",
    "boto3==1.21.46",
    "botocore==1.24.46",
    "s3transfer==0.5.2",
    "six==1.16.0",
    "urllib3==1.26.9",
    "dnspython==2.2.1",
    "pymongo==4.1.1",
    "psycopg2-binary==2.9.3",
    "sshtunnel==0.4.0",
]

if __name__ == "__main__":
    setuptools.setup(
        name="cs-models",
        version="0.0.405",
        author="Harsh Verma",
        author_email="harsh@capitolscience.com",
        description="MySQL db models",
        # long_description=long_description,
        # long_description_content_type='text/markdown',
        url="https://github.com/ezpz76/cs-models",
        packages=setuptools.find_packages(where="src"),
        package_dir={"": "src"},
        classifiers=["Programming Language :: Python :: 3",],
        install_requires=INSTALL_REQUIRES,
        python_requires="~=3.9",
    )
