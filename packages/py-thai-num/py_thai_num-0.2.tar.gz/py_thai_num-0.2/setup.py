from setuptools import setup, find_packages


setup(
    name='py_thai_num',
    version='0.2',
    license='MIT',
    author="Worakrit Sittirit",
    author_email='kritsitti.coe@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/worakrit-sittirit/py_thai_num.git',
    keywords='Thai number to eng',
    description= "python lib for conversion Thai numerical to global numerical.",

)
