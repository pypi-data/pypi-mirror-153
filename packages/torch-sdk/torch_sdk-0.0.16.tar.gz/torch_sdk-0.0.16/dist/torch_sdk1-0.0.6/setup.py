from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3'
]

# description = None
# try:
#     import pypandoc
#     description = pypandoc.convert('README.md', 'rst')
# except (IOError, ImportError):
#     description = open('README.md').read()

setup(
    name='torch_sdk1',
    version='0.0.6',
    description='AccelData Torch SDK.' + '\n\n' + open('README.txt').read(),
    long_description=open('README.md').read() + '\n\n' + open('DATASOURCE_README.md').read() + '\n\n'  + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url='',
    author='acceldata',
    author_email='support@acceldata.io',
    license='Apache Software License',
    classifiers=classifiers,
    keywords='acceldata-torch',
    packages=find_packages(),
    install_requires=['requests', 'dataclasses', 'typing', 'requests-toolbelt']
)
