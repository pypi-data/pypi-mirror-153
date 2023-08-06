from setuptools import setup, find_packages


setup(
    name='flask_br',
    version='0.1.0',
    license='MIT',
    author="Giorgos Myrianthous",
    author_email='giorgos@gmail.com',
    url='https://github.com/gmyrianthous/example-publish-pypi',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='flamba server',
    install_requires=[
          'flask',
          'flask_cors'
      ],

)