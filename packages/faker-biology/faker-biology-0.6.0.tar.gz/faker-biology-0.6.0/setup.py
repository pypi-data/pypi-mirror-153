# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faker_biology',
 'faker_biology._utils',
 'faker_biology.bioseq',
 'faker_biology.mol_biol',
 'faker_biology.physiology',
 'faker_biology.taxonomy',
 'faker_biology.tests']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=12.3.0,<13.0.0', 'faker-python>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'faker-biology',
    'version': '0.6.0',
    'description': 'Fake data from biology',
    'long_description': "# faker-biology\nBiology-related fake data provider for Python Faker\n\nSome providers for biology-related concepts and resources.\n\n## Installation\n\n```\n pip install faker-biology\n```\n\n## Usage:\n\nStandard code to access Faker\n```python\n from faker import Faker\n fake = Faker()\n```\n\n### Physiology: Cell types and  organs\n\n```python\n from faker_biology.physiology import CellType, Organ, Organelle\n\n fake.add_provider(CellType)\n fake.add_provider(Organ)\n fake.add_provider(Organelle)\n \n fake.organ()\n # Sublingual glands\n\n fake.celltype()\n # Centroacinar cell\n\n fake.organelle()\n # chloroplast\n```\n\n### Biosequences\n\n```python\n from faker_biology.bioseq import Bioseq\n\n fake.add_provider(Bioseq)\n\n fake.dna(10)\n # ATCGTGTCAT\n\n fake.rna(10)\n # AUCGUGUCAU\n\n fake.protein(10)\n # MTGHILPSTW\n\n fake.protein_name()\n # HYAL4_HUMAN\n\n fake.amino_acid()\n # AminoAcid(full_name='Glycine', three_letters_name='Gly', one_letter_name='G', mass=57)\n \n fake.amino_acid_name()\n # Glycine\n\n fake.amino_acid_3_letters()\n # Cys\n\n fake.amino_acid_1_letter()\n # W\n\n fake.amino_acid_mass()\n # 103\n```\n\n### Molecular Biology\n\n```python\n from faker_biology.mol_biol import Antibody, RestrictionEnzyme, Enzyme\n\n fake.add_provider(RestrictionEnzyme)\n fake.add_provider(Antibody)\n fake.add_provider(Enzyme)\n\n fake.re()\n # EcoRI\n \n fake.blunt()\n # SmaI\n\n fake.antibody_isotype()\n # IgG\n\n fake.enzyme()\n # Ubiquitin carboxy-terminal hydrolase L1\n\n```\n### Taxonomy \n\n```python\n from faker_biology.taxonomy import ModelOrganism\n\n fake.add_provider(ModelOrganism)\n \n fake.organism()\n # Fission yeast\n\n fake.organism_latin()\n # Schizosaccharomyces pombe\n```\n",
    'author': 'Richard Adams',
    'author_email': 'ra22597@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/richarda23/faker-biology',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
