import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='portfolioscience',
    version='1.0.13',
    description='PortfolioScience RiskAPI Enterprise Client',
    long_description=long_description,
    url='https://www.portfolioscience.com/products/riskapi-enterprise',
    author='Portfolio Science, Inc.',
    author_email='sales@portfolioscience.com',
    packages=['portfolioscience'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "License :: Other/Proprietary License",
    ],
    install_requires=[
          'Cython',
          'pycryptodome',
          'python-dateutil',
    ],    
    python_requires='>=3.7',
)

#if setup never run
#python -m pip install --user --upgrade setuptools wheel
#pip install twine

#cd F:\PortfolioScience\RiskAPI Development\RiskAPI_Client\Enterprise\Enterprise Client Python\Python 3\builds\1.0.xxx\3.7\pip
#update version name in portfolioscience.egg-info file
#python setup.py sdist bdist_wheel

#test pypi
#python -m twine upload --repository testpypi dist/*
#username __token__
#password: copy the API token.

#real pypi
#python -m twine upload dist/*
#username __token__
#password: copy the API token.