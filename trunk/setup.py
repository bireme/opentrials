from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
REQUIREMENTS = open(os.path.join(here, 'requirements.txt')).readlines()

setup(name='bireme-opentrials', version='1.0.17',      
      packages=find_packages(),
      long_description=README + "\n\n" + CHANGES,
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        ],
      keywords='open-trials clinical-trial health application bireme',
      author="BIREME/OPAS/OMS",
      author_email="opentrials-dev@listas.bireme.br",
      url = 'http://reddes.bvsalud.org/projects/clinical-trials/',
      license="LGPL v2.1 (http://www.gnu.org/licenses/lgpl-2.1.txt)",
      install_requires = REQUIREMENTS,
      test_suite='opentrials',
      tests_require=['Nose']
    )