from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='eam-ml',
  version='0.0.3',
  description='A very basic calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='EliteAppMakers',
  author_email='eliteappmakers@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='ml', 
  install_requires=[''],
  packages=['mlpkg'],
  package_dir={'mlpkg': 'mlpkg'},
  package_data={'mlpkg': ['data/*']},
  include_package_data=True
)
