import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='spinthon',
      version='0.21',
      description='A python package intended to simulate spin dynamics',
      url='http://github.com/bennomeier/spinthon',
      author='Benno Meier',
      author_email='meier.benno@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires = [
          'numpy',
          'scipy',
          'spindata'
          ],
      zip_safe=False)
