from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

requirements = []
for line in open('requirements.txt'):
    li = line.strip()
    if not li.startswith('#'):
        requirements.append(line.rstrip())

VERSION = (0, 0, 13)
__version__ = '.'.join(map(str, VERSION))

setup(
    name='sp_piracicaba',
    version=__version__,
    author='Michel Metran',
    author_email='michelmetran@gmail.com',
    description='Compartilhamento de Dados Espaciais',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/open-geodata/sp_piracicaba',
    keywords='python, dados espaciais, geoprocessamento',

    # Python and Packages
    python_requires='>=3',
    install_requires=requirements,

    # Entry
    package_dir={'': 'src'},  # Our packages live under src but src is not a package itself

    # Quando são diversos módulos...
    packages=find_packages('src', exclude=['test']),

    # Dados
    include_package_data=True,
    package_data={'': ['data/output/zips/*.7z']},

    # Classificação
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Portuguese',
        'Intended Audience :: Developers',
    ],
)
