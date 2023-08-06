from django.test import TestCase
from edc_constants.constants import (
    ABSENT,
    NO,
    NORMAL,
    NOT_APPLICABLE,
    NOT_EXAMINED,
    PRESENT,
    YES,
)

from edc_mnsi.models import Mnsi

from .mixins import TestCaseMixin


class TestMnsiModel(TestCaseMixin, TestCase):
    def test_mnsi_calculations_saved_with_best_case_responses(self):
        responses = self.get_best_case_answers()
        model = self.get_mnsi_obj(**responses)

        # Confirm some assumptions about model attributes
        # (both non-calculated and calculated)
        self.assertEqual(model.numb_legs_feet, NO)
        self.assertEqual(model.ankle_reflexes_right_foot, PRESENT)
        self.assertEqual(model.monofilament_left_foot, NORMAL)
        self.assertEqual(model.calculated_patient_history_score, 0)
        self.assertEqual(model.calculated_physical_assessment_score, 0)

        # Retrieve saved object, and confirm the same assumptions hold
        retr_obj = Mnsi.objects.get(id=model.id)
        self.assertEqual(retr_obj.numb_legs_feet, NO)
        self.assertEqual(retr_obj.ankle_reflexes_right_foot, PRESENT)
        self.assertEqual(retr_obj.monofilament_left_foot, NORMAL)
        self.assertEqual(retr_obj.calculated_patient_history_score, 0)
        self.assertEqual(retr_obj.calculated_physical_assessment_score, 0)

    def test_mnsi_calculations_saved_with_mnsi_not_performed_responses(self):
        responses = self.get_mnsi_not_performed_answers()
        model = self.get_mnsi_obj(**responses)

        # Confirm some assumptions about model attributes
        # (both non-calculated and calculated)
        self.assertEqual(model.mnsi_performed, NO)
        self.assertEqual(model.mnsi_not_performed_reason, "e.g. right foot in bandage")
        self.assertEqual(model.numb_legs_feet, NOT_APPLICABLE)
        self.assertEqual(model.ankle_reflexes_right_foot, NOT_EXAMINED)
        self.assertEqual(model.monofilament_left_foot, NOT_EXAMINED)
        self.assertEqual(model.calculated_patient_history_score, 0)
        self.assertEqual(model.calculated_physical_assessment_score, 0)

        # Retrieve saved object, and confirm the same assumptions hold
        retr_obj = Mnsi.objects.get(id=model.id)
        self.assertEqual(retr_obj.mnsi_performed, NO)
        self.assertEqual(retr_obj.mnsi_not_performed_reason, "e.g. right foot in bandage")
        self.assertEqual(retr_obj.numb_legs_feet, NOT_APPLICABLE)
        self.assertEqual(retr_obj.ankle_reflexes_right_foot, NOT_EXAMINED)
        self.assertEqual(retr_obj.monofilament_left_foot, NOT_EXAMINED)
        self.assertEqual(retr_obj.calculated_patient_history_score, 0)
        self.assertEqual(retr_obj.calculated_physical_assessment_score, 0)

    def test_mnsi_calculations_saved_with_worst_case_responses(self):
        responses = self.get_best_case_answers()
        responses.update(self.get_worst_case_patient_history_data())
        responses.update(self.get_worst_case_physical_assessment_data())
        model = self.get_mnsi_obj(**responses)

        # Confirm some assumptions about model attributes
        # (both non-calculated and calculated)
        self.assertEqual(model.numb_legs_feet, YES)
        self.assertEqual(model.ankle_reflexes_right_foot, ABSENT)
        self.assertEqual(model.monofilament_left_foot, ABSENT)
        self.assertEqual(model.calculated_patient_history_score, 13)
        self.assertEqual(model.calculated_physical_assessment_score, 10)

        # Retrieve saved object, and confirm the same assumptions hold
        retr_obj = Mnsi.objects.get(id=model.id)
        self.assertEqual(retr_obj.numb_legs_feet, YES)
        self.assertEqual(retr_obj.ankle_reflexes_right_foot, ABSENT)
        self.assertEqual(retr_obj.monofilament_left_foot, ABSENT)
        self.assertEqual(retr_obj.calculated_patient_history_score, 13)
        self.assertEqual(retr_obj.calculated_physical_assessment_score, 10)
