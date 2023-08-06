import setuptools
import os

setuptools.setup(
    name='toaztr-specs', # Replace with your own username
    version=os.environ['PACKAGE_VERSION'],
    author='Toaztr SAS',
    description='OpenAPI specs of Toaztr',
    long_description=open('../../README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Toaztr/specs',
    project_urls={
        'Bug Tracker': 'https://github.com/Toaztr/specs/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    package_data={'toaztr_specs': ['toaztr.json']}
)
