from setuptools import setup, find_packages


LONG_DESCRIPTION = open('README.rst').read()


setup(
    name='ssm-parameter-store',
    version='0.1',
    description='Simple Python wrapper for getting values from AWS Systems Manager Parameter Store',
    long_description=LONG_DESCRIPTION,
    url='http://github.com/christippett/ssm-parameter-store',
    author='Chris Tippett',
    author_email='chris@spoon.nz',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    zip_safe=False
)
