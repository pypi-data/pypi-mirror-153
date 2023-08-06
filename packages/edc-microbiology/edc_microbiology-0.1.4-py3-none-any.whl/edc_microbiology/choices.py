from edc_constants.constants import IND, NEG, NOT_APPLICABLE, OTHER, POS, UNKNOWN

from .constants import (
    BACTERIA,
    CRYPTOCOCCUS_NEOFORMANS,
    ECOLI,
    KLEBSIELLA_SPP,
    LAM_POS1,
    LAM_POS2,
    LAM_POS3,
    LAM_POS4,
    LAM_POS5,
    NO_GROWTH,
)

BACTERIA_TYPE = (
    (NOT_APPLICABLE, "Not applicable"),
    (ECOLI, "E.coli"),
    (KLEBSIELLA_SPP, "Klebsiella spp."),
    ("streptococcus_pneumoniae", "Streptococcus pneumoniae"),
    ("staphylococus_aureus", "(Sensitive) Staphylococus aureus"),
    ("mrsa", "MRSA"),
    (OTHER, "Other"),
)

BLOOD_CULTURE_RESULTS_ORGANISM = (
    (NOT_APPLICABLE, "Not applicable"),
    (CRYPTOCOCCUS_NEOFORMANS, "Cryptococcus neoformans"),
    (BACTERIA, "Bacteria"),
    ("bacteria_and_cryptococcus", "Bacteria and Cryptococcus"),
    (OTHER, "Other"),
)

BIOPSY_RESULTS_ORGANISM = (
    (CRYPTOCOCCUS_NEOFORMANS, "Cryptococcus neoformans"),
    ("mycobacterium_tuberculosis", "Mycobacterium Tuberculosis"),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

CULTURE_RESULTS = (
    (POS, "Positive"),
    (NO_GROWTH, "No growth"),
    (NOT_APPLICABLE, "Not applicable"),
)

LAM_POS_RESULT = (
    (LAM_POS1, "1+ (low)"),
    (LAM_POS2, "2+"),
    (LAM_POS3, "3+"),
    (LAM_POS4, "4+"),
    (LAM_POS5, "5+ (high)"),
    (UNKNOWN, "Unknown / Grade not reported"),
    (NOT_APPLICABLE, "Not applicable"),
)

URINE_CULTURE_RESULTS_ORGANISM = (
    (NOT_APPLICABLE, "Not applicable"),
    (ECOLI, "E.coli"),
    (KLEBSIELLA_SPP, "Klebsiella spp."),
    (OTHER, "Other"),
)

SPUTUM_GENEXPERT = (
    (POS, "MTB Positive"),
    (NEG, "MTB Negative"),
    (IND, "Indeterminate"),
    (NOT_APPLICABLE, "Not applicable"),
)


SPUTUM_CULTURE = (
    (POS, "MTB Positive"),
    (NEG, "MTB Negative"),
    (IND, "Indeterminate / contaminated"),
    (NOT_APPLICABLE, "Not applicable"),
)
