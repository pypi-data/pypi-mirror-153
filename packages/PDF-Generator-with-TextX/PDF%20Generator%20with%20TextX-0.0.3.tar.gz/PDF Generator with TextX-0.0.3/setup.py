import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "PDF Generator with TextX",
    version = "0.0.3",
    author = "Team 3",
    author_email = "milanatucakov@gmail.com",
    description = ("Developing a DSL for generating PDF files. It could be used in other apps as a tool for generating dynamic reports, contracts, invoices etc."),
    license = "MIT",
    keywords = "textX, PDF, generator, reports, contracts ",
    url = "https://github.com/lukicMilan/JSD-tim3-2021",
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.md'),
    install_requires=["textX[cli]", "Jinja2", "pdfkit", "textX", "wkhtmltopdf"],
    entry_points={
    'console_scripts': [
        'src=src:main',
    ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers"
    ],
)
