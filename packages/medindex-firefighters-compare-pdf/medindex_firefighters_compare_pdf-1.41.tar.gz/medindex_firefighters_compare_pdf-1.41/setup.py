import setuptools


def get_install_requires():
    with open('requirements.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]


DESCRIPTION = "A package for internal usage in The Medindex ru for pdf image compare"


setuptools.setup(
    name="medindex_firefighters_compare_pdf",
    version="1.41",
    author='kurzeneva.o',
    author_email='kurzeneva.o@medindex.ru',
    description=DESCRIPTION,
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    #install_requires=get_install_requires(),
)
