import setuptools


VERSION = "2.2.1"

setuptools.setup(
    name='CosmoTech-SupplyChain',
    version=VERSION,
    author='Alexis Fossart',
    author_email='alexis.fossart@cosmotech.com',
    url='https://github.com/Cosmo-Tech/supplychain-python-library<',
    license='MIT',
    packages=setuptools.find_packages(),
    description='A support package for SupplyChain',
    long_description="A support package for Cosmotech SupplyChain",
    install_requires=[
        "azure-core",
        "azure-digitaltwins-core",
        "azure-identity",
        "azure-kusto-data",
        "azure-kusto-ingest",
        "azure-storage-queue",
        "azure-storage-blob",
        "CosmoTech-Acceleration-Library",
        "cma",
        "jsonschema",
        "numpy",
        "openpyxl",
        "pandas",
        "python-dateutil",
        "pytest"
    ]
)
