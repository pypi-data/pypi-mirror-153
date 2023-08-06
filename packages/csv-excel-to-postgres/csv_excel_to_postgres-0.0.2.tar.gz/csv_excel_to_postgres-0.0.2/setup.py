import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csv_excel_to_postgres",
    version="0.0.2",
    author="KSV Muralidhar",
    license="MIT",
    author_email="murali_dhar0552@yahoo.com",
    description="Export CSV/Excel to PostgreSQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "pandas==1.3.4",
        "numpy==1.21.5",
        "psycopg2==2.9.3",
        "xlrd==2.0.1",
        "openpyxl==3.0.9"
    ],
    python_requires=">=3.7"
)
