from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Caribe',
  version='0.5.4',
  description='Trinidad English Creole to Standard English',
  long_description_content_type="text/markdown",
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Keston Smith',
  author_email='keston.smith@my.uwi.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='Translator', 
  packages=find_packages(),
  install_requires=['nltk==3.6.3', 'pandas==1.3.4', 'gingerit==0.8.2', 'transformers==4.15.0'] 
)