from setuptools import setup, find_packages

# The text of the README file
with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name='drivebox',
    version='0.1.2',
    license='MIT',
    author="César J. Lockhart de la Rosa",
    author_email='lockhart@imec.be',
    description="API for the Caonabo DribeBox (CDB)",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    url='https://github.imec.be/dna-storage/drivebox',
    keywords='Switch Matriox, Potentiostat, Galvanostat, SMU, MUX, api, caonabo',
    install_requires=['pyserial', 'time', 'math', 'numpy', 'xlrd', 'matplotlib', 'datetime'],
    python_requires='>=3'
)