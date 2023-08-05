from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='intpolylib',
    version='0.2.1',
    author="Dariusz Libecki",
    author_email='dariuszlibecki@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Kerad20/polylib',
    keywords='polynomials',
    install_requires=[
          'numpy',
      ],

)