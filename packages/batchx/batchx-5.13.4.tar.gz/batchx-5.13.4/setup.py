from setuptools import setup

# Set doc for package
with open("package-doc.md", "r") as fh:
    long_description = fh.read()

# Set package version
version = '0.0.0'
with open('version') as f:
    version = f.readline().strip()


setup(name='batchx',
      version=version,
      description='Batchx Python API',
      long_description=long_description,
      author='Batchx',
      author_email='dev@batchx.com',
      url='https://github.com/batchx/api',
      packages=['batchx'],
      install_requires=[
          'grpcio', 'PyJWT==1.7.1', 'retry', 'google-api-python-client'
      ])
