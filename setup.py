from setuptools import setup

setup(name='pageinfo',
      version='0.40',
      description='Tool for extracting basic information from web pages',
      url='https://github.com/nytlabs/pageinfo',
      keywords='metadata title web page url description twitter facebook',
      author='Alexis Lloyd',
      author_email='alexislloyd@gmail.com',
      license='Apache',
      packages=['pageinfo'],
       install_requires=[
          'beautifulsoup4',
          'lxml',
          'requests'
      ],
      zip_safe=False)
