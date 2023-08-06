from setuptools import setup

setup(
    name='summarytable',
    version='0.1.7',
    author='Dale Kreitler',
    author_email='dkreitler@bnl.gov',
    packages=['summarytable',],
    scripts=['bin/summarytable',
             'bin/summarytable_ap',
             'bin/summarytable_offline',],
    url='https://www.github.com/dalekreitler-bnl/summarytable',
    license='LICENSE.txt',
    description='Gathering MX processing summaries',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "xmltodict",
    ],
    python_requires='>=3.6',
)
