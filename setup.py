from os.path import dirname, join
from setuptools import setup, find_packages

from ircbot import get_version

def fread(fname):
    return open(join(dirname(__file__), fname)).read()

setup(
    name='ircbot',
    version=get_version(),
    description="A Python IRC Bot",
    long_description=fread('README.markdown'),
    author='George Hickman',
    license='MIT License',
    url='http://github.com/incuna/ircbot/',
    packages=find_packages(),
    scripts=['ircbot/ircbot'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Eiffel Forum License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ],
)

