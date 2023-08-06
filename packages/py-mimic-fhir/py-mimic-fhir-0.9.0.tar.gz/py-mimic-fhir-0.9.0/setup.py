from setuptools import setup, find_packages

setup(
    name='py-mimic-fhir',
    version='0.9.0',
    author='Alex Bennett, KinD Labs, The Hospital For Sick Children',
    packages=find_packages(exclude=['tests', 'tests.*']),
    description='A package to help convert MIMIC to FHIR',
    install_requires=['pandas', 'numpy', 'requests', 'psycopg2>=2.86']
)
