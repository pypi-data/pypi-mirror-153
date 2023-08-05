# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leximpact_prepare_data']

package_data = \
{'': ['*']}

install_requires = \
['OpenFisca-France>=113.0.0,<114.0.0',
 'leximpact-aggregates>=0.0.5,<0.0.6',
 'leximpact-socio-fisca-simu-etat>=0.1.2,<0.2.0',
 'pandas>=1.3.0,<2.0.0',
 'typing-extensions>=3.10.0,<4.0.0',
 'vaex-jupyter>=0.7.0,<0.8.0',
 'vaex-server>=0.8.1,<0.9.0']

extras_require = \
{':extra == "pipeline"': ['scikit-learn[pipeline]>=1.0.1,<2.0.0',
                          'diagrams[pipeline]>=0.20.0,<0.21.0',
                          'vaex-core[pipeline]>=4.8.0,<5.0.0',
                          'tables[pipeline]>=3.6.1,<4.0.0',
                          'python-dotenv[pipeline]>=0.19.2,<0.20.0']}

setup_kwargs = {
    'name': 'leximpact-prepare-data',
    'version': '0.0.17',
    'description': 'Prepare data for LexImpact',
    'long_description': "# LexImpact Prepare Data\n\n\n\nCe projet regroupe les scripts permettant de préparer les données des différents projets [Leximpact](https://leximpact.an.fr).\n\n## Schéma complet de préparation et d'utilisation des données\n![LexImpact Pipeline](notebooks/schemas/leximpact_pipeline.png)\n\n\n    \nLe pipeline prepare-data est donc le suivant :\n\nInput: erfs_flat_2018.h5\n\n### 01_db_reduce.ipynb   \nObjectif: Réduit le nombre de variables dans la base\n\nOutput: 01_erfs_reduced_2018.h5\n\n### 02_db_enlarge.ipynb\nObjectif: Ajoute des gens fictifs dans la base pour pouvoir calibrer\n\n\nOutput: 02_erfs_enlarged_2018.h5\n\n\n### 03_db_add_rfr.ipynb\nInput : CalibPote-2018-revkire.json\n\nObjectifs: \n-\tCalculer le RFR dans OpenFisca\n-\tCalibrer le RFR ERFS_2018 sur POTE_2018\n\nOutput: 03_erfs_rfr_2018.h5\n\n\n### 04_db_add_var\n0403_db_add_var_copules.ipynb\n\n0401_db_add_var_copules-algo_monte-carlo.ipynb  \n\n\n0402_db_add_var_copules-validate.ipynb\n\nInput : ExportCopule-2018-variable.json\n\nObjectif: Ajoute les variables issues de POTE 2018 dans la base ERFS 2018\n\nOutput:  04_erfs_var_copules_2018.h5\n\n\n### 05_db_calib_var_copules.ipynb\n\nInput : CalibPote-2019-variable.json\n\nObjectifs: \n-\tVieillit la base ERFS_2018 vers 2019 (nos données les plus récentes) : inflation économique et inflation des foyers\n-\tCalibre chacune des variables issues de POTE sur POTE 2019\n\nOutput:  05_erfs_calibrated_ff_2018_to_2019.h5\n\n### 06_db_aging_final.ipynb\nObjectifs:\n\n-\tVieillit la base ERFS_2019 vers 2021 (année voulue pour les calculs) : inflation économique et inflation des foyers\n-\tBruitage statistique de la base pour anonymisation\n\nOutput: 06_erfs_ff_2018_aged_2021.h5\n\n    \n\n# How to contribute\n\nPlease see the [contributing page](https://documentation.leximpact.dev/leximpact_prepare_data/contributing).\n",
    'author': 'LexImpact',
    'author_email': 'leximpact@an.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://leximpact.an.fr/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
