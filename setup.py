from setuptools import setup, find_packages


LONG_DESCRIPTION = open('README.md').read()


setup(
    name='ssm-parameter-store',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Simple Python wrapper for getting values from AWS Systems Manager Parameter Store',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='http://github.com/christippett/ssm-parameter-store',
    author='Chris Tippett',
    author_email='chris@spoon.nz',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=['boto3'],
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
