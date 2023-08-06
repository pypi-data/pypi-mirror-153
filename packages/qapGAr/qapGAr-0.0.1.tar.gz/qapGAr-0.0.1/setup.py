from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python'
]
 
setup(
  name='qapGAr',
  version='0.0.1',
  description='genetic algorithm library for quadratic assignment problem',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Rūta Buckiūnaitė',
  author_email='aneliukee@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['genetic', 'algorithm', 'quadratic', 'assignment'],
  packages=find_packages(),
  install_requires=['']
)