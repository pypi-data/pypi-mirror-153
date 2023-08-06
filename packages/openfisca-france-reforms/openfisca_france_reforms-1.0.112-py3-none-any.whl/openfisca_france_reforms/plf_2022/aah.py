from openfisca_france.model.base import (
    ADD,
    Famille,
    Individu,
    max_,
    min_,
    set_input_divide_by_period,
    MONTH,
    Variable,
    where,
)


class aah_base_ressources(Variable):
    value_type = float
    label = "Base ressources de l'allocation adulte handicapé"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        law = parameters(period)

        en_activite = individu("salaire_imposable", period) > 0

        def assiette_conjoint(revenus_conjoint):
            return 0.9 * (1 - 0.2) * revenus_conjoint

        def assiette_revenu_activite_demandeur(revenus_demandeur):
            smic_brut_annuel = (
                12
                * law.marche_travail.salaire_minimum.smic.smic_b_horaire
                * law.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel
            )
            tranche1 = min_(0.3 * smic_brut_annuel, revenus_demandeur)
            tranche2 = revenus_demandeur - tranche1
            return (1 - 0.8) * tranche1 + (1 - 0.4) * tranche2

        def base_ressource_eval_trim():
            three_previous_months = period.first_month.start.period("month", 3).offset(
                -3
            )
            base_ressource_activite = individu(
                "aah_base_ressources_activite_eval_trimestrielle", period
            ) - individu(
                "aah_base_ressources_activite_milieu_protege",
                three_previous_months,
                options=[ADD],
            )
            base_ressource_hors_activite = individu(
                "aah_base_ressources_hors_activite_eval_trimestrielle", period
            ) + individu(
                "aah_base_ressources_activite_milieu_protege",
                three_previous_months,
                options=[ADD],
            )

            base_ressource_demandeur = (
                assiette_revenu_activite_demandeur(base_ressource_activite)
                + base_ressource_hors_activite
            )

            base_ressource_demandeur_conjoint = individu.famille.demandeur(
                "aah_base_ressources_activite_eval_trimestrielle", period
            ) + individu.famille.demandeur(
                "aah_base_ressources_hors_activite_eval_trimestrielle", period
            )
            base_ressource_conjoint_conjoint = individu.famille.conjoint(
                "aah_base_ressources_activite_eval_trimestrielle", period
            ) + individu.famille.conjoint(
                "aah_base_ressources_hors_activite_eval_trimestrielle", period
            )
            base_ressource_conjoint = (
                base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR)
                + base_ressource_demandeur_conjoint
                * individu.has_role(Famille.CONJOINT)
            )

            return base_ressource_demandeur + assiette_conjoint(base_ressource_conjoint)

        def base_ressource_eval_annuelle():
            base_ressource = individu("aah_base_ressources_eval_annuelle", period)

            base_ressource_demandeur_conjoint = individu.famille.demandeur(
                "aah_base_ressources_eval_annuelle", period
            )
            base_ressource_conjoint_conjoint = individu.famille.conjoint(
                "aah_base_ressources_eval_annuelle", period
            )
            base_ressource_conjoint = (
                base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR)
                + base_ressource_demandeur_conjoint
                * individu.has_role(Famille.CONJOINT)
            )

            return assiette_revenu_activite_demandeur(
                base_ressource
            ) + assiette_conjoint(base_ressource_conjoint)

        return where(
            en_activite,
            base_ressource_eval_trim() / 12,
            base_ressource_eval_annuelle() / 12,
        )

    def formula_2022(individu, period, parameters):
        law = parameters(period)
        aah_parameters = parameters(
            period
        ).prestations_sociales.prestations_etat_de_sante.invalidite.aah

        en_activite = individu("salaire_imposable", period) > 0

        def assiette_conjoint(revenus_conjoint):
            return 0.9 * (1 - aah_parameters.abattement_conjoint) * revenus_conjoint

        def assiette_revenu_activite_demandeur(revenus_demandeur):
            smic_brut_annuel = (
                12
                * law.marche_travail.salaire_minimum.smic.smic_b_horaire
                * law.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel
            )
            tranche1 = min_(0.3 * smic_brut_annuel, revenus_demandeur)
            tranche2 = revenus_demandeur - tranche1
            return (1 - 0.8) * tranche1 + (1 - 0.4) * tranche2

        def base_ressource_eval_trim():
            three_previous_months = period.first_month.start.period("month", 3).offset(
                -3
            )
            base_ressource_activite = individu(
                "aah_base_ressources_activite_eval_trimestrielle", period
            ) - individu(
                "aah_base_ressources_activite_milieu_protege",
                three_previous_months,
                options=[ADD],
            )
            base_ressource_hors_activite = individu(
                "aah_base_ressources_hors_activite_eval_trimestrielle", period
            ) + individu(
                "aah_base_ressources_activite_milieu_protege",
                three_previous_months,
                options=[ADD],
            )

            base_ressource_demandeur = (
                assiette_revenu_activite_demandeur(base_ressource_activite)
                + base_ressource_hors_activite
            )

            base_ressource_demandeur_conjoint = individu.famille.demandeur(
                "aah_base_ressources_activite_eval_trimestrielle", period
            ) + individu.famille.demandeur(
                "aah_base_ressources_hors_activite_eval_trimestrielle", period
            )
            base_ressource_conjoint_conjoint = individu.famille.conjoint(
                "aah_base_ressources_activite_eval_trimestrielle", period
            ) + individu.famille.conjoint(
                "aah_base_ressources_hors_activite_eval_trimestrielle", period
            )
            base_ressource_conjoint = (
                base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR)
                + base_ressource_demandeur_conjoint
                * individu.has_role(Famille.CONJOINT)
            )
            # Enlève les abattement forfaitaires aux revenus du conjoint.
            # https://www.banquedesterritoires.fr/aah-le-plf-2022-tranche-pour-un-abattement-forfaitaire
            af_nbenf = individu.famille("af_nbenf", period)
            base_ressource_conjoint_abattue = max_(
                0,
                base_ressource_conjoint
                - (
                    aah_parameters.abattement_conjoint_salarie_forfait
                    + af_nbenf
                    * aah_parameters.abattement_conjoint_salarie_forfait_enfant
                ),
            )

            return base_ressource_demandeur + assiette_conjoint(
                base_ressource_conjoint_abattue
            )

        def base_ressource_eval_annuelle():
            base_ressource = individu("aah_base_ressources_eval_annuelle", period)

            base_ressource_demandeur_conjoint = individu.famille.demandeur(
                "aah_base_ressources_eval_annuelle", period
            )
            base_ressource_conjoint_conjoint = individu.famille.conjoint(
                "aah_base_ressources_eval_annuelle", period
            )
            base_ressource_conjoint = (
                base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR)
                + base_ressource_demandeur_conjoint
                * individu.has_role(Famille.CONJOINT)
            )
            # Enlève les abattement forfaitaires aux revenus du conjoint.
            # https://www.banquedesterritoires.fr/aah-le-plf-2022-tranche-pour-un-abattement-forfaitaire
            af_nbenf = individu.famille("af_nbenf", period)
            base_ressource_conjoint_abattue = max_(
                0,
                base_ressource_conjoint
                - (
                    aah_parameters.abattement_conjoint_salarie_forfait
                    + af_nbenf
                    * aah_parameters.abattement_conjoint_salarie_forfait_enfant
                ),
            )

            return assiette_revenu_activite_demandeur(
                base_ressource
            ) + assiette_conjoint(base_ressource_conjoint_abattue)

        return where(
            en_activite,
            base_ressource_eval_trim() / 12,
            base_ressource_eval_annuelle() / 12,
        )
