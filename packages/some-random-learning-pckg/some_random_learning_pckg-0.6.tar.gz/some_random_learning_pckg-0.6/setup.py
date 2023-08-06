from setuptools import setup, find_packages


setup(
    name='some_random_learning_pckg',
    version='0.6',
    license='MIT',
    author="Tabba",
    author_email='email@example.com',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    url='https://github.com/pyrootml/',
    keywords='example project',
    install_requires=[
      ],

)
