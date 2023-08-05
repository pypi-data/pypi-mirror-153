from setuptools import setup, find_packages


setup(
    name='intpolylib',
    version='0.2',
    author="Dariusz Libecki",
    author_email='dariuszlibecki@gmail.com',
    license='MIT',
    long_description='README.md',
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Kerad20/polylib',
    keywords='polynomials',
    install_requires=[
          'numpy',
      ],

)