import setuptools

# 第三方依赖包及版本
requires = [
    'chardet>=3.0.4',
    'dataclasses>=0.7',
    'Twisted>=20.3.0',
    'urllib3>=1.22',
    'PyMySQL>=0.9.2',
    'psutil>=5.4.5',
    'requests>=2.18.4',
    'xlrd>=1.1.0',
    'colorama>=0.3.9',
    'pandas>=0.23.0',
    'six>=1.11.0',
    'pywin32>=223',
    'tushare>=1.2.60',
    'numpy>=1.14.3',
    'stompest.async>=2.3.0',
    # 'TA_Lib>=0.4.18',
    'scipy>=1.1.0',
    'grpcio>=1.29.0',
    'backports.statistics>=0.1.0',
    'beautifulsoup4>=4.9.3',
    'cached_property>=1.5.2',
    'pymongo',
    'manga>=0.1.13',
    'protobuf>=3.14.0',
    'pycryptodome>=3.9.9',
    'python_dateutil>=2.8.1',
    'redis>=3.5.3',
    'rqalpha>=4.2.4',
    'rqdatac>=2.9.15',
    'stompest>=2.3.0'
]

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(name='tmqc',
    version='0.1.7',
    description='tian ma quant cloud',
    author='tmqc',
    author_email='tmqc@gmail.com',
    url="https://github.com/tmqc/tmqc",
    license='LGPT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='==3.6.5',
    install_requires = requires,
    include_package_data=True,
    zip_safe=False)