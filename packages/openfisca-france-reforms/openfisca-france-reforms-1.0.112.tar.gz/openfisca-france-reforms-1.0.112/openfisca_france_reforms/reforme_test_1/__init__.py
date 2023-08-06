import os

from openfisca_core.parameters import load_parameter_file
from openfisca_core.reforms import Reform


def modify_parameters(parameters):
    parameters_dir = os.path.join(os.path.dirname(__file__), "parameters")
    for yaml_split_path in walk_dir(parameters_dir, []):
        split_name = yaml_split_path.copy()
        id = split_name[-1].replace(".yaml", "")
        split_name[-1] = id
        parameter = load_parameter_file(
            os.path.join(parameters_dir, *yaml_split_path),
            name=".".join(split_name),
        )
        parent = parameters
        for parent_id in split_name[:-1]:
            child = getattr(parent, parent_id, None)
            assert (
                child is not None
            ), f'Parameter "{parent.name}" has no "{parent_id}" child'
            parent = child
        parent.children[id] = parameter
        setattr(parent, id, parameter)

    return parameters


def walk_dir(root_dir, relative_split_dir):
    dir = os.path.join(root_dir, *relative_split_dir)
    for entry in os.scandir(dir):
        if entry.name.startswith("."):
            continue
        relative_split_path = relative_split_dir + [entry.name]
        if entry.is_dir():
            yield from walk_dir(root_dir, relative_split_path)
        else:
            if not entry.name.endswith(".yaml"):
                continue
            yield relative_split_path


class ReformeTest1(Reform):
    name = "Réforme de test n°1"
    tax_benefit_system_name = "openfisca_france"

    def apply(self):
        self.modify_parameters(modifier_function=modify_parameters)
