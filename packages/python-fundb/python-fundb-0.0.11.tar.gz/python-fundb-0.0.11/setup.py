import setuptools


def long_description():
    with open('README.md', 'r') as file:
        return file.read()


setuptools.setup(
    name='python-fundb',
    version='0.0.11',
    author='Mardix',
    author_email='mardix@blackdevhub.io',
    description='FunDB: Hybrid Row-and-Document Oriented datastore leveraging SQL/RDBMS database: SQLite, MySQL, MariaDB, Postgresql ',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/mardix/fundb',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
    ],
    python_requires='>=3.8.0',
    install_requires = [
        "pymysql",
        "sqlparams",
        "DBUtils"
    ],
    packages=['fundb'],
    package_dir={'':'src'}
)
