from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()



setup(
    name='spotiboost',
    packages=find_packages(),
    include_package_data=True,
    version='3.7.1',
    description='A free and open-source spotify followers increaser package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Adarsh Goel',
    author_email='contact@adarsh.codes',
    url='https://github.com/adarsh-goel/spotiboost',
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    install_requires='requests==2.27.1',
    license='GPL',
    entry_points={
            'console_scripts': [
                'spotiboost = adarsh:spotiboost',
            ],
    },
    python_requires='>=3.5'
)
