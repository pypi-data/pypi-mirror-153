import pathlib
from setuptools import setup, find_packages

current_dir = pathlib.Path(__file__).parent.resolve()

long_description = (current_dir / 'README.md').read_text(encoding='utf-8')

setup(

    name = 'Pras_Server',
    version = '1.0.6',
    description='A webserver to repair PDB files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.protein-science.com/',
    author='Osita S. Nnyigide',
    author_email='osita@protein-science.com',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['Pras_Server',],
    include_package_data=True,
    python_requires='>=3.6, <4',
    install_requires=['numpy','matplotlib','setuptools'],
    package_data={'Pras_Server': ['KD.dat']},
)
