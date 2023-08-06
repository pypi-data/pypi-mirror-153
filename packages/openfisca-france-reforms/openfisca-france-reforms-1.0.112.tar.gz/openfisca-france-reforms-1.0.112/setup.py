# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openfisca_france_reforms',
 'openfisca_france_reforms.landais_piketty_saez',
 'openfisca_france_reforms.lfi_progressivite_bareme_impot_revenu',
 'openfisca_france_reforms.plf_2022',
 'openfisca_france_reforms.plf_2022.scripts',
 'openfisca_france_reforms.reforme_test_1']

package_data = \
{'': ['*'],
 'openfisca_france_reforms.plf_2022': ['parameters/impot_revenu/*',
                                       'parameters/impot_revenu/abattements_rni/enfant_marie/*',
                                       'parameters/impot_revenu/decote/*',
                                       'parameters/impot_revenu/plafond_qf/*',
                                       'parameters/prestations_sociales/prestations_etat_de_sante/invalidite/aah/*',
                                       'tests_apres_reforme/*',
                                       'tests_avant_reforme/*'],
 'openfisca_france_reforms.reforme_test_1': ['parameters/impot_revenu/bareme_ir_depuis_1945/*']}

install_requires = \
['openfisca-france>=116.7.3']

entry_points = \
{'openfisca.reforms': ['reforme_test_1 = '
                       'openfisca_france_reforms.reforme_test_1:ReformeTest1']}

setup_kwargs = {
    'name': 'openfisca-france-reforms',
    'version': '1.0.112',
    'description': 'Some reforms for French OpenFisca tax-benefit system',
    'long_description': None,
    'author': 'Emmanuel Raviart',
    'author_email': 'emmanuel@raviart.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.leximpact.dev/leximpact/openfisca-france-reforms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
