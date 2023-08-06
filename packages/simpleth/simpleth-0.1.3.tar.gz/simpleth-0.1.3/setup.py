from setuptools import setup, find_packages

setup(
    name='simpleth',
    version='0.1.3',
    author='Stephen Newell',
    author_email='<snewell4@gmail.com>',
    description='Simplified Ethereum for Python',
    long_description=open('README.rst').read(),
    url='https://github.com/snewell4/simpleth',
    packages=find_packages(),
    python_requires='>=3.8',    # adds Type.Final
    install_requires=[
        'web3.py>=5.23.0'       # adds maxPriorityFeePerGas
        ],
    keywords='blockchain, ganache, Solidity, ethereum, smart-contract',
    include_package_data=True,  # see manifest.ini
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Other/Nonlisted Topic'
        ]
    )
