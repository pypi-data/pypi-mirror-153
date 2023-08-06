from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import NO, NOT_APPLICABLE, OTHER, POS, YES
from edc_registration.models import RegisteredSubject
from edc_utils import get_utcnow
from edc_visit_schedule.constants import DAY1

from edc_microbiology.constants import (
    BACTERIA,
    CRYPTOCOCCUS_NEOFORMANS,
    KLEBSIELLA_SPP,
    NO_GROWTH,
)
from edc_microbiology.form_validators import MicrobiologyFormValidator

from ..models import Appointment, SubjectVisit


class TestMicrobiologyFormValidator(TestCase):
    def setUp(self):
        self.subject_identifier = "1234"
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            randomization_datetime=get_utcnow(),
        )
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code=DAY1,
        )
        self.subject_visit = SubjectVisit.objects.create(
            appointment=appointment, subject_identifier=self.subject_identifier
        )

    def test_urine_culture_performed_yes_require_urine_culture_result(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "urine_culture_performed": YES,
            "urine_culture_date": get_utcnow(),
            "urine_culture_result": NOT_APPLICABLE,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("urine_culture_result", form_validator._errors)

    def test_urine_culture_performed_no_require_urine_culture_result(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "urine_culture_performed": NO,
            "urine_culture_result": NO_GROWTH,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_urine_culture_performed_na_given_urine_culture_result(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "urine_culture_performed": YES,
            "urine_culture_result": NOT_APPLICABLE,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_urine_culture_result_none_urine_culture_organism(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "urine_culture_result": POS,
            "urine_culture_organism": NOT_APPLICABLE,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("urine_culture_organism", form_validator._errors)

    def test_pos_urine_results_na_urine_culture_organism(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "urine_culture_result": POS,
            "urine_culture_organism": NOT_APPLICABLE,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_urine_results_with_urine_culture_organism(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "urine_culture_result": POS,
            "urine_culture_organism": KLEBSIELLA_SPP,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_other_urine_culture_result_require_urine_organism_other(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "urine_culture_organism": OTHER,
            "urine_culture_organism_other": None,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("urine_culture_organism_other", form_validator._errors)

    def test_yes_blood_culture_performed_none_blood_culture_results(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_performed": YES,
            "blood_culture_date": get_utcnow(),
            "blood_culture_result": NOT_APPLICABLE,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("blood_culture_result", form_validator._errors)

    def test_no_blood_culture_performed_none_blood_culture_results(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_performed": NO,
            "blood_culture_result": POS,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("blood_culture_result", form_validator._errors)

    def test_no_blood_culture_performed_with_blood_culture_results(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_performed": NO,
            "blood_culture_result": NO_GROWTH,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_blood_culture_results_require_date_blood_taken(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_result": POS,
            "blood_culture_date": None,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_blood_culture_results_require_blood_culture_organism(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_result": POS,
            "blood_culture_date": get_utcnow().date(),
            "blood_culture_day": 1,
            "blood_culture_organism": NOT_APPLICABLE,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("blood_culture_organism", form_validator._errors)

    def test_pos_blood_culture_results_na_blood_culture_organism(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_result": POS,
            "blood_culture_organism": NOT_APPLICABLE,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_blood_culture_organism_require_culture_organism_other(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_organism": OTHER,
            "blood_culture_organism_other": None,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_blood_culture_organism_na_culture_organism_other(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_organism": CRYPTOCOCCUS_NEOFORMANS,
            "blood_culture_organism_other": CRYPTOCOCCUS_NEOFORMANS,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_blood_culture_organism_with_culture_organism_other(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_organism": OTHER,
            "blood_culture_organism_other": "other organism",
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_blood_organism_is_bacteria_require_bacteria_identified(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_organism": BACTERIA,
            "blood_culture_bacteria": NOT_APPLICABLE,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("blood_culture_bacteria", form_validator._errors)

    def test_blood_organism_is_bacteria_na_bacteria_identified(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_organism": NOT_APPLICABLE,
            "blood_culture_bacteria": KLEBSIELLA_SPP,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("blood_culture_bacteria", form_validator._errors)

    def test_other_bacteria_identified_require_bacteria_identified_other(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_bacteria": OTHER,
            "blood_culture_bacteria_other": None,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_bacteria_identified_na_bacteria_identified_other(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "blood_culture_bacteria": OTHER,
            "blood_culture_bacteria_other": None,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_sputum_results_culture_require_sputum_result(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "sputum_culture_performed": YES,
            "sputum_culture_result": None,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_sputum_results_culture_with_sputum_results_positive(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "sputum_culture_result": POS,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_tissue_biopsy_performed_require_tissue_biopsy_result(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "tissue_biopsy_performed": YES,
            "tissue_biopsy_result": None,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_no_tissue_biopsy_performed_none_tissue_biopsy_result(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "tissue_biopsy_performed": NO,
            "tissue_biopsy_result": POS,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("tissue_biopsy_result", form_validator._errors)

    def no_test_tissue_biopsy_performed_with_tissue_biopsy_result(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "tissue_biopsy_performed": NO,
            "tissue_biopsy_result": NO_GROWTH,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_tissue_biopsy_result_none_biopsy_date(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "tissue_biopsy_performed": NO,
            "tissue_biopsy_date": get_utcnow().date(),
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_tissue_biopsy_result_na_tissue_biopsy_date(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "tissue_biopsy_performed": YES,
            "tissue_biopsy_date": None,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("tissue_biopsy_date", form_validator._errors)

    def test_pos_tissue_biopsy_result_with_tissue_biopsy_day(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "tissue_biopsy_performed": YES,
            "tissue_biopsy_date": get_utcnow(),
            "tissue_biopsy_result": POS,
            "tissue_biopsy_day": None,
        }
        form = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("tissue_biopsy_day", form._errors)

    def test_pos_tissue_biopsy_result_none_tissue_biopsy_organism(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "tissue_biopsy_performed": YES,
            "tissue_biopsy_date": get_utcnow(),
            "tissue_biopsy_result": POS,
            "tissue_biopsy_organism": None,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_tissue_biopsy_result_na_tissue_biopsy_organism(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "tissue_biopsy_result": POS,
            "tissue_biopsy_organism": NOT_APPLICABLE,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_tissue_biopsy_org_none_tissue_biopsy_org_other(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "tissue_biopsy_organism": OTHER,
            "tissue_biopsy_organism_other": None,
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_tissue_biopsy_org_with_tissue_biopsy_org_other(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "tissue_biopsy_organism": OTHER,
            "tissue_biopsy_organism_other": "some tissue organism",
        }
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")
