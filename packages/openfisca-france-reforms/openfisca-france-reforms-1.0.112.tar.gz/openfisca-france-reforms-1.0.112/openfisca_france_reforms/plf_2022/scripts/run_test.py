#! /usr/bin/env python

import os
import sys

from openfisca_core.tools.test_runner import run_tests

from openfisca_france import FranceTaxBenefitSystem

from .. import Plf2022


def main():
    options = {}

    tax_benefit_system = FranceTaxBenefitSystem()
    reform = Plf2022(tax_benefit_system)
    reform_path = os.path.abspath(os.path.join("openfisca_france_reforms", "plf_2022"))

    # Excute tests before reform.
    before_reform_paths = [
        os.path.join(reform_path, relative_path)
        for relative_path in ["tests_avant_reforme"]
    ]
    tax_benefit_system_code = run_tests(
        tax_benefit_system,
        before_reform_paths,
        options,
    )
    if tax_benefit_system_code == 5:
        # Ignore error that occurs when "no tests ran".
        tax_benefit_system_code = 0

    # Excute tests after reform.
    after_reform_paths = [
        os.path.join(reform_path, relative_path)
        for relative_path in ["tests_apres_reforme"]
    ]
    reform_code = run_tests(reform, after_reform_paths, options)
    if reform_code == 5:
        # Ignore error that occurs when "no tests ran".
        reform_code = 0

    sys.exit(tax_benefit_system_code if tax_benefit_system_code != 0 else reform_code)


if __name__ == "__main__":
    sys.exit(main())
