import setuptools
import os
import re


# Read XGEE version
VERSIONFILE="xgee/xgee.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    XGEE_VERSION = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

xgee_files = ['meta/layout.ecore']
xgee_files.extend(package_files('xgee/core'))

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()
requirements_path=str(Path('__file__').parent)+'/requirements.txt'
if os.path.isfile(requirements_path):
        with open(requirements_path) as f:
            install_requires = f.read().splitlines()

allpackages=setuptools.find_packages()

setuptools.setup(
    packages=setuptools.find_packages(),
    name='XGEE',
    version=XGEE_VERSION,
    author='Matthias Brunner',
    author_email='matthias.brunner@ils.uni-stuttgart.de',
    description='eXtensible Graphical EMOF Editor - a framework for graphical editing single page web-applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/xgee/py/xgee',
    entry_points={
    'console_scripts': [
        'xgee = xgee.__main__:main',
    ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
    ],    
    install_requires=install_requires,
    python_requires='>=3.6',
    include_package_data=True,
    package_data={'xgee': xgee_files},
)
