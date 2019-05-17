import setuptools
from collections import OrderedDict

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SayTeX",
    version="0.1.4",
    author="Arvid Lunnemark",
    author_email="arvid.lunnemark@gmail.com",
    description="Convert natural language math expressions into well-formatted LaTeX.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://saytex.xyz",
    project_urls=OrderedDict((
        ('Documentation', 'https://saytex.readthedocs.io'),
        ('Code', 'https://github.com/arvid220u/saytex')
    )),
    packages=setuptools.find_packages(),
    package_data={
        'saytex.saytexsyntax': ['saytex_dictionary/*.json'],
        'saytex.layers': ['synonym_standardization_dictionary.json']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)