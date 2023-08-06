from setuptools import setup, find_packages

setup(
    name='mycryptowallet-deskent',
    version='0.0.4',
    author='Deskent',
    author_email='battenetciz@gmail.com',
    description='My Crypt Wallet library',
    install_requires=[
        'bitcoinlib==0.6.4',
        'myloguru-deskent'
    ],
    scripts=['src/crypto_wallet/crypto_wallet.py'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Deskent/my_cryptowallet",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)
