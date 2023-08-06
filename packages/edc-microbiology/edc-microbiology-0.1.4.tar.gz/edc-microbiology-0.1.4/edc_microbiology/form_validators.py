from edc_constants.constants import OTHER, POS, YES
from edc_form_validators import FormValidator
from edc_form_validators.extra_mixins import StudyDayFormValidatorMixin

from .constants import BACTERIA


class BloodCultureFormValidatorMixin:
    def validate_blood_culture(self: FormValidator):
        self.required_if(
            YES, field="blood_culture_performed", field_required="blood_culture_date"
        )

        self.applicable_if(
            YES,
            field="blood_culture_performed",
            field_applicable="blood_culture_result",
        )

        self.required_if(POS, field="blood_culture_result", field_required="blood_culture_day")

        self.applicable_if(
            POS,
            field="blood_culture_result",
            field_applicable="blood_culture_organism",
        )

        self.validate_other_specify(
            field="blood_culture_organism",
            other_specify_field="blood_culture_organism_other",
            other_stored_value=OTHER,
        )

        condition = (
            self.cleaned_data.get("blood_culture_organism") == BACTERIA
            or self.cleaned_data.get("blood_culture_organism") == "bacteria_and_cryptococcus"
        )
        self.applicable_if_true(condition=condition, field_applicable="blood_culture_bacteria")

        self.validate_other_specify(
            field="blood_culture_bacteria",
            other_specify_field="blood_culture_bacteria_other",
            other_stored_value=OTHER,
        )


class BloodCultureSimpleFormValidatorMixin:
    def validate_blood_culture(self: FormValidator):

        self.required_if(
            YES, field="blood_culture_performed", field_required="blood_culture_date"
        )

        self.applicable_if(
            YES,
            field="blood_culture_performed",
            field_applicable="blood_culture_result",
        )

        self.required_if(
            POS,
            field="blood_culture_result",
            field_required="blood_culture_organism_text",
        )


class CsfGenexpertFormValidator:
    def validate_csf_genexpert(self: FormValidator):
        self.required_if(
            YES,
            field="csf_genexpert_performed",
            field_required="csf_genexpert_date",
        )

        self.applicable_if(
            YES,
            field="csf_genexpert_performed",
            field_applicable="csf_result_genexpert",
        )


class HistopathologyFormValidatorMixin:
    def validate_histopathology(self: FormValidator, exclude_fields=None):
        exclude_fields = exclude_fields or []

        self.required_if(
            YES, field="tissue_biopsy_performed", field_required="tissue_biopsy_date"
        )

        self.applicable_if(
            YES,
            field="tissue_biopsy_performed",
            field_applicable="tissue_biopsy_result",
        )

        if "tissue_biopsy_day" not in exclude_fields:
            self.required_if(
                POS, field="tissue_biopsy_result", field_required="tissue_biopsy_day"
            )

        self.applicable_if(
            POS,
            field="tissue_biopsy_result",
            field_applicable="tissue_biopsy_organism",
        )

        self.validate_other_specify(
            field="tissue_biopsy_organism",
            other_specify_field="tissue_biopsy_organism_other",
            other_stored_value=OTHER,
        )


class UrineCultureFormValidatorMixin:
    def validate_urine_culture(self: FormValidator):
        self.required_if(
            YES, field="urine_culture_performed", field_required="urine_culture_date"
        )

        self.applicable_if(
            YES,
            field="urine_culture_performed",
            field_applicable="urine_culture_result",
        )

        self.applicable_if(
            POS,
            field="urine_culture_result",
            field_applicable="urine_culture_organism",
        )

        self.validate_other_specify(
            field="urine_culture_organism",
            other_specify_field="urine_culture_organism_other",
            other_stored_value=OTHER,
        )


class SputumCultureFormValidatorMixin:
    def validate_sputum_culture(self: FormValidator):
        self.required_if(
            YES, field="sputum_culture_performed", field_required="sputum_culture_date"
        )
        self.applicable_if(
            YES, field="sputum_culture_performed", field_applicable="sputum_culture_result"
        )


class SputumAfbFormValidatorMixin:
    def validate_sputum_afb(self: FormValidator):
        self.required_if(YES, field="sputum_afb_performed", field_required="sputum_afb_date")
        self.applicable_if(
            YES, field="sputum_afb_performed", field_applicable="sputum_afb_result"
        )


class SputumGenexpertFormValidatorMixin:
    def validate_sputum_genexpert(self: FormValidator):
        self.required_if(
            YES,
            field="sputum_genexpert_performed",
            field_required="sputum_genexpert_date",
        )
        self.applicable_if(
            YES,
            field="sputum_genexpert_performed",
            field_applicable="sputum_genexpert_result",
        )


class UrinaryLamFormValidatorMixin:
    def validate_urinary_lam(self: FormValidator):
        self.required_if(
            YES,
            field="urinary_lam_performed",
            field_required="urinary_lam_date",
        )

        self.applicable_if(
            YES,
            field="urinary_lam_performed",
            field_applicable="urinary_lam_result",
        )

        self.applicable_if(
            POS,
            field="urinary_lam_result",
            field_applicable="urinary_lam_result_grade",
        )


class MicrobiologyFormValidator(
    StudyDayFormValidatorMixin,
    UrinaryLamFormValidatorMixin,
    SputumGenexpertFormValidatorMixin,
    SputumCultureFormValidatorMixin,
    SputumAfbFormValidatorMixin,
    BloodCultureFormValidatorMixin,
    HistopathologyFormValidatorMixin,
    UrineCultureFormValidatorMixin,
    FormValidator,
):
    def clean(self):
        self.validate_study_day_with_datetime(
            subject_identifier=self.cleaned_data.get("subject_visit").subject_identifier,
            study_day=self.cleaned_data.get("day_blood_taken"),
            compare_date=self.cleaned_data.get("blood_taken_date"),
            study_day_field="day_blood_taken",
        )

        self.validate_study_day_with_datetime(
            subject_identifier=self.cleaned_data.get("subject_visit").subject_identifier,
            study_day=self.cleaned_data.get("day_biopsy_taken"),
            compare_date=self.cleaned_data.get("biopsy_date"),
            study_day_field="day_biopsy_taken",
        )

        self.validate_urinary_lam()

        self.validate_sputum_afb()

        self.validate_sputum_culture()

        self.validate_sputum_genexpert()

        self.validate_blood_culture()

        self.validate_histopathology()

        self.validate_urine_culture()
