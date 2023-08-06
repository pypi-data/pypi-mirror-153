from os import path

from setuptools import setup

INSTALL_REQUIRES = [
    'pyOpenSSL>=21.0.0',
    'python-dateutil~=2.8.2',
    'plogger>=1.0.6'
]

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pycert',
    version='1.0.3',
    packages=['pycert'],
    url='https://github.com/c-pher/certificate',
    license='GNU General Public License v3.0',
    author='Andrey Komissarov',
    author_email='a.komisssarov@gmail.com',
    description='The cross-platform tool to get certificate info (including self-signed).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
)
