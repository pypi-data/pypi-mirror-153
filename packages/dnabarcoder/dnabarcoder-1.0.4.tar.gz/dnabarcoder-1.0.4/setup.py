from setuptools import setup, find_packages


setup(
    name='dnabarcoder',
    version='1.0.4',
    license='Apache License 2.0',
    author="Duong Vu",
    author_email='duong.t.vu@gmail.com',
    package_dir={'': 'src'},
    packages=['dnabarcoder','dnabarcoder.analysis','dnabarcoder.prediction','dnabarcoder.visualization','dnabarcoder.aidscripts','dnabarcoder.classification'],
    url='https://github.com/vuthuyduong/dnabarcoder',
    keywords='dnabarcoder',
    install_requires=[
          'scikit-learn',
	  'scipy==1.2.1',
	  'numpy==1.16.2',
      ],
    include_package_data=True,
)
