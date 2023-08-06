from setuptools import setup, find_packages
from pathlib import Path

path = Path(__file__).resolve().parent

setup(name='treedir',
      version="04.06.2022",
      description='TreeDir to define simple directory structures',
      url='http://gitlab.csn.uchile.cl/dpineda/treedir',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      install_requires=['click', 'anytree',],
      scripts=[
      ],
      entry_points={
      },
      packages=find_packages(),
      include_package_data=True,
      license='GPLv3',
      long_description="Tree Dir base class",
      long_description_content_type='text/markdown',
      zip_safe=False)
