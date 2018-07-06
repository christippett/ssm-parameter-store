from setuptools import setup, find_packages


setup(
    name='ssm-parameter-store',
    version='0.1',
    description='Python wrapper for storing secrets in AWS Systems Manager Parameter Store',
    url='http://github.com/christippett/ssm-parameter-store',
    author='Chris Tippett',
    author_email='chris@spoon.nz',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False
)
