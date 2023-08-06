import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cosecurity-utility-internal-lib',
    version='0.0.21',
    description='Built-in utility library for application development by the CoSecurity infrastructure',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'psycopg2==2.9.3',
        'boto3==1.21.36'
    ]    
)