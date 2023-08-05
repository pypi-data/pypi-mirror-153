from setuptools import setup, find_packages
import os
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / "readme.md").read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = ["virtualenv", "GitPython", "click"]

    if env and env == "dev":
        return dependency

    return dependency + ['PF-PY-YMLEnv', 'PF-PY-File', 'PF-PY-Text']


setup(
    name='PF-PWeb-SourceMan',
    version='1.0.5',
    url='https://github.com/problemfighter/pf-pweb-sourceman',
    license='Apache 2.0',
    author='Problem Fighter',
    author_email='problemfighter.com@gmail.com',
    description='PWeb Project source management tool by Problem Fighter',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    entry_points={
        'console_scripts': [
            'pwebsm=pf_pweb_sourceman.cli_main:bsw'
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ]
)