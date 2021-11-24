from setuptools import setup

setup(name='wordninja',
  version="0.1.0",
  packages = ['wordninja'],
  package_dir={'wordninja': 'wordninja'},
  package_data={'wordninja': ['models/default_model.txt.gz']},
  include_package_data=True,
)
