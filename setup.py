from setuptools import setup, find_packages

with open('requirements.txt') as fd:
    setup(name='dockerize',
          version='1',
          packages=find_packages(),
          install_requires=fd.readlines(),
          package_data={'dockerize': ['templates/*']},
          entry_points={
              'console_scripts': [
                  'dockerize = dockerize.main:main',
              ],
          }
          )
