import os
from setuptools import setup

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name='feather',
    version='0.1',
    license='AGPL-3.0',
    author="Hugh O'Reilly",
    author_email='horeilly1101@gmail.com',
    url='https://github.com/hack-rice/feather',
    description='A minimalist API for interacting with the quill registration tool.',
    packages=['feather', 'feather.email', 'feather.csv'],
    test_suite="tests",
)
