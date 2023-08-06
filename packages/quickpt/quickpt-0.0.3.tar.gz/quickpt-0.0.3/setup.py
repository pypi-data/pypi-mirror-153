from setuptools import setup, find_packages

classifiers = [
  'Programming Language :: Python :: 3',
  'License :: OSI Approved :: MIT License',
  'Operating System :: OS Independent'
]


setup(
  name='quickpt',
  version='0.0.3',
  author='Youssef Sultan',
  author_email='youssefsultann@gmail.com',
  description='For aggregating and visualizing variance, unique values and percent of missing values of features in any dataset.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  license='MIT',
  classifiers=classifiers,
  keywords='visualize',
  packages=find_packages(),
  install_requires=['pandas', 'numpy', 'scikit-learn', 'plotly'],
  url ='https://github.com/youssefsultan/quickpt'
)