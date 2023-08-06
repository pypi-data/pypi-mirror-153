"""Setup file for itango."""

import platform
from setuptools import setup, find_packages


def get_entry_points():
    major = int(platform.python_version_tuple()[0])
    name = 'itango3' if major == 3 else 'itango'
    return {
        "console_scripts": ["{0} = itango:run".format(name)],
        "gui_scripts": ["{0}-qt = itango:run_qt".format(name)]}


CLASSIFIERS = """\
Framework :: IPython
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: System :: Shells
""".splitlines()


setup(
    name='itango',
    use_scm_version=True,
    setup_requires=["setuptools_scm"],

    packages=find_packages(),
    package_data={'itango': [
        'resource/*.png', 'resource/*.svg']},
    entry_points=get_entry_points(),
    install_requires=[
        'IPython>=1.0',
        'pytango>=9.2.0',
        'packaging'],

    license='LGPL',
    classifiers=CLASSIFIERS,
    author='Tiago Coutinho',
    author_email="coutinho@esrf.fr",
    description='An interactive Tango client',
    long_description=open('README.rst').read(),
    url='https://gitlab.com/tango-controls/itango',
    download_url='http://pypi.python.org/pypi/itango',
    platforms=['Linux', 'Windows XP/Vista/7/8'],
    keywords=['PyTango', 'IPython'],
    )
