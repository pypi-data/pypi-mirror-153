from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.0.10'
DESCRIPTION = 'Reverse Engineering of My Etisalat App'
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()
# Setting up
setup(
    name="etpy",
    version=VERSION,
    author="TarekTurbo (Tarek Abdelraheem)",
    author_email="<tarekthedream@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[i.split("==")[0] for i in """pydantic==1.9.0
requests==2.27.1
setuptools==58.1.0
xmltodict==0.12.0""".split("\n")],
    keywords=['python', 'Reverse', 'Enginner', 'My Etisalat', 'Internet in egypt',"egpt","etisalat","masr", "etisalat masr"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)