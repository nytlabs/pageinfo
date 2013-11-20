from setuptools import setup

setup(name='pageinfo',
      version='0.1',
      description='Tool for extracting basic information from web pages',
      url='https://github.com/nytlabs/pageinfo',
      keywords='metadata title web page url description twitter facebook',
      author='Alexis Lloyd',
      author_email='alexislloyd@gmail.com',
      license='Apache',
      packages=['pageinfo'],
       install_requires=[
          'beautifulsoup4',
          'requests',
          'lxml'
      ],
      zip_safe=False)