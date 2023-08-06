from setuptools import setup, find_packages


setup(
    name='AutoLayout',
    version='0.1.3',
    license='MIT',
    author="Tin Tran",
    author_email='trantin0815@gmail.com',
    packages=["AutoLayout"],
    url='https://github.com/trezitorul/GDSPYUtils/tree/AutoLayout-package/AutoLayout',
    keywords='AutoLayout',
    install_requires=[
          'rectpack', 'gdspy'
      ],

)