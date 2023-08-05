from setuptools import setup


with open("VERSION", "r") as fp:
    version = fp.read().strip("\n")

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cnside',
    version=version,
    install_requires=required,
    packages=['cnside', 'cnside.cli', 'cnside.errors', 'cnside.objects', 'cnside.metadata', 'cnside.documents',
              'cnside.authenticator', 'cnside.storage', 'cnside.parsers'],
    package_dir={'': 'src'},
    entry_points={
        "console_scripts": [
            "cnside=cnside.cli.main:main"
        ]
    },
    url='https://illustria.io',
    license='Proprietary',
    author='Bogdan Kortnov',
    author_email='bogdan@illustria.io',
    description='CNSIDE Command Line Interface Tool'
)
