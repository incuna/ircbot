from os.path import dirname, join
from setuptools import setup, find_packages

from phenny import get_version

def fread(fname):
    return open(join(dirname(__file__), fname)).read()

setup(
    name='phenny',
    version=get_version(),
    description="A Python IRC Bot",
    long_description=fread('README.markdown'),
    author='Sean B. Palmer',
    license='Eiffel Forum License 2',
    url='http://inamidst.com/phenny/',
    packages=find_packages(),
    scripts=['phenny/phenny'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Eiffel Forum License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ],
)

