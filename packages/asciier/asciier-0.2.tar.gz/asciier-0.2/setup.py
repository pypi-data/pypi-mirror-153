from setuptools import setup, find_packages


setup(
    name='asciier',
    version='0.2',
    license='MIT',
    author="yuxontop",
    author_email='yqrs.tktk@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/yuxontop/Image2Ascii',
    keywords='image ascii',
    install_requires=[
          'pillow',
      ],

)