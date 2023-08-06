def get_blood_culture_fieldset():
    return [
        "Blood Culture",
        {
            "fields": (
                "blood_culture_performed",
                "blood_culture_date",
                "blood_culture_day",
                "blood_culture_result",
                "blood_culture_organism",
                "blood_culture_organism_other",
                "blood_culture_bacteria",
                "blood_culture_bacteria_other",
            )
        },
    ]


def get_csf_fieldset():
    return [
        "CSF Microbiology",
        {
            "fields": (
                "csf_genexpert_performed",
                "csf_genexpert_date",
                "csf_genexpert_result",
            )
        },
    ]


def get_histopathology_fieldset():
    return [
        "Histopathology",
        {
            "fields": (
                "tissue_biopsy_performed",
                "tissue_biopsy_date",
                "tissue_biopsy_day",
                "tissue_biopsy_result",
                "tissue_biopsy_organism",
                "tissue_biopsy_organism_other",
                "tissue_biopsy_report",
            )
        },
    ]


def get_sputum_afb_fieldset():
    return [
        "Sputum AFB",
        {
            "fields": (
                "sputum_afb_performed",
                "sputum_afb_date",
                "sputum_afb_result",
            )
        },
    ]


def get_sputum_culture_fieldset():
    return [
        "Sputum culture",
        {
            "fields": (
                "sputum_culture_performed",
                "sputum_culture_date",
                "sputum_culture_result",
            )
        },
    ]


def get_sputum_genexpert_fieldset():
    return [
        "Sputum Gene-Xpert",
        {
            "fields": (
                "sputum_genexpert_performed",
                "sputum_genexpert_date",
                "sputum_genexpert_result",
            )
        },
    ]


def get_urinary_lam_fieldset():
    return [
        "Urinary LAM",
        {
            "fields": (
                "urinary_lam_performed",
                "urinary_lam_date",
                "urinary_lam_result",
                "urinary_lam_result_grade",
            ),
        },
    ]


def get_urine_culture_fieldset():
    return [
        "Urine Culture (Only for patients with >50 white cells in urine)",
        {
            "fields": (
                "urine_culture_performed",
                "urine_culture_date",
                "urine_culture_result",
                "urine_culture_organism",
                "urine_culture_organism_other",
            )
        },
    ]
