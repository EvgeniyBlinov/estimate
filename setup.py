from setuptools import setup, find_packages
from os.path import join, dirname

# parse_requirements() returns generator of pip.req.InstallRequirement objects

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

#install_reqs = parse_requirements('requirements.txt')
with open('estimate/_version.py') as f:  exec(f.read())

setup(
    name='estimate',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    #install_requires=install_reqs,
    entry_points={
        'console_scripts': ['estimate=estimate.command_line:main'],
    }
)
