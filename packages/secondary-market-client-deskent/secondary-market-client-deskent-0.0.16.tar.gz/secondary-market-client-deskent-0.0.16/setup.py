from setuptools import setup, find_packages
setup(
    name='secondary-market-client-deskent',
    version='0.0.16',
    author='Deskent',
    author_email='battenetciz@gmail.com',
    description='Secondary market',
    install_requires=[
        'aiohttp==3.8.1',
        'python-dotenv==0.19.2',
        'selenium-wire==4.6.2',
        'selenium~=4.1.5',
        'webdriver-manager==3.7.0',
        'myloguru-deskent~=0.0.9'
    ],
    scripts=['src/secondary_market/main.py'],
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
    url="https://github.com/Deskent/secondary_market_client",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)
