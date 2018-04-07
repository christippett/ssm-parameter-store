from setuptools import setup

setup(
    name='ssm-parameter-store',
    version='0.1',
    description='Python wrapper for storing secrets in AWS Systems Manager Parameter Store',
    url='http://github.com/christippett/ssm-parameter-store',
    author='Chris Tippett',
    author_email='c.tippett@gmail.com',
    license='MIT',
    packages=['ssm_parameter_store'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=False
)
