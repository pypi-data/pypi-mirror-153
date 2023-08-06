from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: Apache Software License',
  'Programming Language :: Python :: 3'
]

setup(
  name='torch_airflow_sdk',
  version='0.0.27',
  description='AccelData Torch Airflow SDK.' + '\n\n' + open('README.txt').read(),
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type="text/markdown",
  url='',
  author='acceldata',
  author_email='support@acceldata.io',
  license='Apache Software License',
  classifiers=classifiers,
  keywords='acceldata-torch',
  packages=find_packages(),
  install_requires=['requests', 'dataclasses', 'typing']
)