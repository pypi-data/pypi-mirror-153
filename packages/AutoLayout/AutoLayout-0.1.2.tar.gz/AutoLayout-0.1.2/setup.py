from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='AutoLayout',
    version='0.1.2',
    license='MIT',
    author="Tin Tran",
    author_email='trantin0815@gmail.com',
    packages=find_packages('AutoLayout'),
    package_dir={'': 'AutoLayout'},
    url='https://github.com/trezitorul/GDSPYUtils/tree/AutoLayout-package/AutoLayout',
    keywords='AutoLayout',
    install_requires=[
          'rectpack', 'gdspy'
      ],

)