import setuptools
from pathlib import Path

setuptools.setup(
    name="clioexlsx",
    version='1.2',
    description="Compare worksheet or workbook, then highlight the different rows or cells on book 2 and then generate the output file. This module uses Pandas and XLWings",
    keywords=["xlsx", "compare excel"],
    long_description=Path("README.md").read_text(),
    author='Cheny Lioe',
    author_email='chenylioe@yahoo.com',
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
