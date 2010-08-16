from setuptools import setup, find_packages

setup(
    name = "bireme-opentrials",
    version = "1.0",
    url = 'http://reddes.bvsalud.org/projects/clinical-trials/', #see also: http://github.com/bireme/opentrials
    license = 'GPL',
    description = "",
    author = 'Bireme',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)

