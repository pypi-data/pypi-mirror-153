from setuptools import setup,find_packages
classifiers=[
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
setup(
  name='maxfancyprint',
  version='0.0.1',
  description='Fancy way of printing things',
  Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Max-Emil Hansen',
  author_email='max8han@gmail.com',
  License='MIT',
  classifiers=classifiers,
  keywords='print',
  packages=find_packages(),
  install_requires=['']
)