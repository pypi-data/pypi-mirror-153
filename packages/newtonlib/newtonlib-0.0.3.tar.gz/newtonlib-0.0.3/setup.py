from setuptools import setup, find_packages

setup(
    name='newtonlib',
    version='0.0.3',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Python package for a university course',
    long_description=open('README.md').read(),
    package_data={
        "": ["*.pyd", "*.dll"],
    },
    # install_requires=['requests'],
    url='https://git.e-science.pl/kwazny_252716_dpp/kwazny252716_pythonnative',
    author='Karol Ważny',
    author_email='kwazny_252716@e-science.pl'
)
