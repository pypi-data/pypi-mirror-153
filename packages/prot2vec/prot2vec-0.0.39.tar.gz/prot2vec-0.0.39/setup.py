from setuptools import setup, find_packages

VERSION = '0.0.39'
DESCRIPTION = 'Vectorization and Annotation of Protein Sequences'
LONG_DESCRIPTION = 'A package that allows to vectorize and annotate protein sequences.'

# Setting up
setup(
    name="prot2vec",
    version=VERSION,
    author="Tomas Honzik",
    author_email="<tomas.honziik@seznam.cz>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'protein'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
