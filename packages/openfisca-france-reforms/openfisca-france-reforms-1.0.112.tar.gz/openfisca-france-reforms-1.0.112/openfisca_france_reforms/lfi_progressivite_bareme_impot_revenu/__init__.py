# Une réforme de test du barème de l'impôt sur le revenu
# Tirée d'un amendement de La France Insoumise
# https://www.assemblee-nationale.fr/dyn/15/amendements/2272A/CION_FIN/CF1391

import os

from openfisca_core.parameters import load_parameter_file
from openfisca_core.reforms import Reform


def modify_parameters(parameters):
    reform_parameters = load_parameter_file(
        os.path.join(os.path.dirname(__file__), "parameters.yaml"),
        name="impot_revenu.bareme",
    )
    parameters.impot_revenu.children["bareme"] = reform_parameters
    parameters.impot_revenu.bareme = reform_parameters
    return parameters


class LfiProgressiviteBaremeImpotRevenu(Reform):
    name = "Amendement LFI pour une progressivité du barème de l'impôt sur le revenu"
    tax_benefit_system_name = "openfisca_france"

    def apply(self):
        self.modify_parameters(modifier_function=modify_parameters)
