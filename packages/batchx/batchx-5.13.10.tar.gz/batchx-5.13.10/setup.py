from setuptools import setup

# Set package version
version = '0.0.0'
with open('version') as f:
    version = f.readline().strip()

try:
  import pypandoc
  long_description = pypandoc.convert_file('README.md', 'rst')
  print(long_description)
except(IOError, ImportError):
  long_description = open('README.md').read()

setup(name='batchx',
      version=version,
      description='Batchx Python API',
      long_description=long_description,
      author='Batchx',
      author_email='dev@batchx.com',
      url='https://github.com/batchx/api',
      packages=['batchx'],
      install_requires=[
          'grpcio', 'PyJWT', 'retry', 'google-api-python-client'
      ])
