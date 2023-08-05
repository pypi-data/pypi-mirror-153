from setuptools import setup, find_packages

setup(
    name='mycryptowallet-deskent',
    version='0.0.1',
    author='Deskent',
    author_email='battenetciz@gmail.com',
    description='My Crypt Wallet library',
    install_requires=[
        'myloguru-deskent',
        'bitcoinlib==0.6.4',
        'pytest==7.1.2',
        'pytest-aio==1.4.1',
    ],
    scripts=['src/crypto_wallet/crypto_wallet.py'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Deskent/my_cryptowallet",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)
