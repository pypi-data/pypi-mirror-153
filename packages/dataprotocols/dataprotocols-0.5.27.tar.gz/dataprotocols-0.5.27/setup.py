from setuptools import setup, find_packages
from pathlib import Path

path = Path(__file__).resolve().parent

with open(path/'README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(path/'VERSION') as version_file:
    version = version_file.read().strip()

setup(name='dataprotocols',
      version=version,
      description='DataProtocols is a set of classes that implement protocols for data acquisition',
      url='http://gitlab.csn.uchile.cl/dpineda/dataprotocols',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      install_requires=[
	'Click', 
	'networktools', 
	'basic-logtools',
	"rich", 
	"pyinstrument"],
      scripts=[
          'dataprotocols/scripts/gsof.py',
          'dataprotocols/scripts/eryo.py',
          'dataprotocols/scripts/protocol.py',
      ],
      entry_points={
          'console_scripts': ["gsof = dataprotocols.scripts.gsof:run_gsof",
                              "eryo = dataprotocols.scripts.eryo:run_eryo",
                              "protocol = dataprotocols.scripts.protocol:run_protocol"]
      },
      packages=find_packages(),
      include_package_data=True,
      license='GPLv3',
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
