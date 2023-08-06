from copy import deepcopy

from django.test import TestCase
from edc_constants.constants import NO, NORMAL, NOT_EXAMINED, OTHER, PRESENT, YES
from edc_form_validators import FormValidatorTestCaseMixin

from edc_mnsi.calculator import (
    MnsiPatientHistoryCalculatorError,
    MnsiPhysicalAssessmentCalculatorError,
)
from edc_mnsi.form_validator import MnsiFormValidator
from edc_mnsi.forms import MnsiForm
from edc_mnsi.models import AbnormalFootAppearanceObservations

from .mixins import TestCaseMixin


class TestMnsiFormValidator(FormValidatorTestCaseMixin, TestCaseMixin, TestCase):

    form_validator_default_form_cls = MnsiFormValidator

    def test_valid_best_case_form_ok(self):
        cleaned_data = deepcopy(self.get_best_case_answers())
        form = MnsiForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_valid_mnsi_not_performed_form_ok(self):
        cleaned_data = deepcopy(self.get_mnsi_not_performed_answers())
        form = MnsiForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_physical_assessment_questions_not_applicable_if_mnsi_not_performed(self):
        for foot_choice in self.foot_choices:
            for question_field in [
                f"normal_appearance_{foot_choice}_foot",
                f"ulceration_{foot_choice}_foot",
                f"ankle_reflexes_{foot_choice}_foot",
                f"vibration_perception_{foot_choice}_toe",
                f"monofilament_{foot_choice}_foot",
            ]:
                # Setup test case
                cleaned_data = deepcopy(self.get_mnsi_not_performed_answers())
                # set one field as answered, e.g. != NOT_EXAMINED
                cleaned_data.update(
                    {
                        question_field: self.get_best_case_answers()[question_field],
                    }
                )

                # Test
                with self.subTest(foot_choice=foot_choice, question_field=question_field):
                    form_validator = self.validate_form_validator(cleaned_data)
                    self.assertIn(question_field, form_validator._errors)
                    self.assertIn(
                        "Invalid. "
                        "Expected `not examined` if MNSI assessment was not performed.",
                        str(form_validator._errors.get(question_field)),
                    )
                    self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

    def test_valid_worst_case_form_ok(self):
        cleaned_data = deepcopy(self.get_best_case_answers())
        cleaned_data.update(self.get_worst_case_patient_history_data())
        cleaned_data.update(self.get_worst_case_physical_assessment_data())
        form = MnsiForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_foot_amputated_returns_false_if_foot_normal_appearance(self):
        for foot_choice in self.foot_choices:
            with self.subTest(foot_choice=foot_choice):
                cleaned_data = deepcopy(self.get_best_case_answers())
                cleaned_data.update(
                    {
                        f"normal_appearance_{foot_choice}_foot": YES,
                        f"abnormal_obs_{foot_choice}_foot": self.get_nonempty_abnormal_obs_set(
                            "deformity_amputation"
                        ),
                    }
                )
                form_validator = self.form_validator_default_form_cls(
                    cleaned_data=cleaned_data
                )
                self.assertFalse(form_validator.foot_amputated(foot_choice))

    def test_foot_amputated_returns_false_if_no_abnormalities_on_foot(self):
        for foot_choice in self.foot_choices:
            with self.subTest(foot_choice=foot_choice):
                cleaned_data = deepcopy(self.get_best_case_answers())
                cleaned_data.update(
                    {
                        f"normal_appearance_{foot_choice}_foot": NO,
                        f"abnormal_obs_{foot_choice}_foot": self.get_empty_abnormal_obs_set(),
                    }
                )
                form_validator = self.form_validator_default_form_cls(
                    cleaned_data=cleaned_data
                )
                self.assertFalse(form_validator.foot_amputated(foot_choice))

    def test_foot_amputated_returns_false_if_abnormality_not_amputated(self):
        for foot_choice in self.foot_choices:
            with self.subTest(foot_choice=foot_choice):
                cleaned_data = deepcopy(self.get_best_case_answers())
                cleaned_data.update(
                    {
                        f"normal_appearance_{foot_choice}_foot": NO,
                        f"abnormal_obs_{foot_choice}_foot": self.get_nonempty_abnormal_obs_set(
                            "infection"
                        ),
                    }
                )
                form_validator = self.form_validator_default_form_cls(
                    cleaned_data=cleaned_data
                )
                self.assertFalse(form_validator.foot_amputated(foot_choice))

    def test_foot_amputated_returns_true_if_foot_amputated(self):
        for foot_choice in self.foot_choices:
            for amputated_obs_set in self.amputated_abnormal_obs_sets:
                with self.subTest(
                    foot_choice=foot_choice,
                    abnormal_obs=amputated_obs_set,
                ):
                    cleaned_data = {
                        f"normal_appearance_{foot_choice}_foot": NO,
                        f"abnormal_obs_{foot_choice}_foot": amputated_obs_set,
                    }
                    form_validator = self.form_validator_default_form_cls(
                        cleaned_data=cleaned_data
                    )
                    self.assertTrue(form_validator.foot_amputated(foot_choice))

    def test_physical_assessment_questions_applicable_if_foot_not_amputated(self):
        for foot_choice in self.foot_choices:
            for question_field in [
                f"ulceration_{foot_choice}_foot",
                f"ankle_reflexes_{foot_choice}_foot",
                f"vibration_perception_{foot_choice}_toe",
                f"monofilament_{foot_choice}_foot",
            ]:
                # Setup test case
                cleaned_data = self.get_best_case_answers()
                cleaned_data.update({question_field: NOT_EXAMINED})

                # Test
                with self.subTest(foot_choice=foot_choice, question_field=question_field):
                    form_validator = self.validate_form_validator(cleaned_data)
                    self.assertIn(question_field, form_validator._errors)
                    self.assertIn(
                        "Invalid. "
                        "Examination result expected if MNSI assessment was performed.",
                        str(form_validator._errors.get(question_field)),
                    )
                    self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

    def test_physical_assessment_questions_applicable_if_foot_abnormality_but_not_amputated(
        self,
    ):
        for foot_choice in self.foot_choices:
            for question_field in [
                f"ulceration_{foot_choice}_foot",
                f"ankle_reflexes_{foot_choice}_foot",
                f"vibration_perception_{foot_choice}_toe",
                f"monofilament_{foot_choice}_foot",
            ]:
                # Setup test case
                cleaned_data = self.get_best_case_answers()
                cleaned_data.update(
                    {
                        # Specify foot abnormal appearance, not-amputated
                        f"normal_appearance_{foot_choice}_foot": NO,
                        f"abnormal_obs_{foot_choice}_foot": self.get_nonempty_abnormal_obs_set(
                            "infection"
                        ),
                    }
                )
                cleaned_data.update({question_field: NOT_EXAMINED})

                # Test
                with self.subTest(foot_choice=foot_choice, question_field=question_field):
                    form_validator = self.validate_form_validator(cleaned_data)
                    self.assertIn(question_field, form_validator._errors)
                    self.assertIn(
                        "Invalid. "
                        "Examination result expected if MNSI assessment was performed.",
                        str(form_validator._errors.get(question_field)),
                    )
                    self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

    def test_physical_assessment_questions_not_required_if_foot_amputated(self):
        for foot_choice in self.foot_choices:
            for amputated_obs_set in self.amputated_abnormal_obs_sets:
                with self.subTest(foot_choice=foot_choice, abnormal_obs=amputated_obs_set):
                    cleaned_data = deepcopy(self.get_best_case_answers())
                    cleaned_data.update(
                        {
                            # Specify foot abnormal appearance, amputated
                            f"normal_appearance_{foot_choice}_foot": NO,
                            f"abnormal_obs_{foot_choice}_foot": amputated_obs_set,
                            # Skip other physical assessment answers
                            f"ulceration_{foot_choice}_foot": NOT_EXAMINED,
                            f"ankle_reflexes_{foot_choice}_foot": NOT_EXAMINED,
                            f"vibration_perception_{foot_choice}_toe": NOT_EXAMINED,
                            f"monofilament_{foot_choice}_foot": NOT_EXAMINED,
                        }
                    )

                    form_validator = self.validate_form_validator(cleaned_data)
                    self.assertEqual(form_validator._errors, {})

    def test_physical_assessment_questions_still_allowed_if_foot_amputated(self):
        for foot_choice in self.foot_choices:
            for amputated_obs_set in self.amputated_abnormal_obs_sets:
                with self.subTest(foot_choice=foot_choice, abnormal_obs=amputated_obs_set):
                    cleaned_data = self.get_best_case_answers()
                    cleaned_data.update(
                        {
                            # Specify foot abnormal appearance, amputated
                            f"normal_appearance_{foot_choice}_foot": NO,
                            f"abnormal_obs_{foot_choice}_foot": amputated_obs_set,
                            # Skip other physical assessment answers
                            f"ulceration_{foot_choice}_foot": PRESENT,
                            f"ankle_reflexes_{foot_choice}_foot": PRESENT,
                            f"vibration_perception_{foot_choice}_toe": PRESENT,
                            f"monofilament_{foot_choice}_foot": NORMAL,
                        }
                    )

                    form_validator = self.validate_form_validator(cleaned_data)
                    self.assertEqual(form_validator._errors, {})

    def test_abnormal_observations_required_if_foot_appearance_not_normal(self):
        cleaned_data = deepcopy(self.get_best_case_answers())

        for foot_choice in self.foot_choices:
            field = f"normal_appearance_{foot_choice}_foot"
            m2m_field = f"abnormal_obs_{foot_choice}_foot"

            with self.subTest(
                f"Testing '{m2m_field}' is required if {field}='No'",
                field=field,
                m2m_field=m2m_field,
            ):
                cleaned_data.update({field: NO})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertIn(m2m_field, form_validator._errors)
                self.assertIn(
                    "This field is required",
                    str(form_validator._errors.get(m2m_field)),
                )
                self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

                # Set back to YES, and move on to next test
                cleaned_data.update({field: YES})

    def test_abnormal_observations_accepted_if_foot_appearance_not_normal(self):
        cleaned_data = deepcopy(self.get_best_case_answers())
        m2m_field_selection = AbnormalFootAppearanceObservations.objects.filter(
            name="infection"
        )

        for foot_choice in self.foot_choices:
            field = f"normal_appearance_{foot_choice}_foot"
            m2m_field = f"abnormal_obs_{foot_choice}_foot"

            with self.subTest(
                f"Testing '{m2m_field}' accepted if {field}='No'",
                field=field,
                m2m_field=m2m_field,
            ):
                cleaned_data.update({field: NO, m2m_field: m2m_field_selection})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertEqual(form_validator._errors, {})

    def test_abnormal_observations_not_applicable_if_foot_appearance_is_normal(self):
        cleaned_data = deepcopy(self.get_best_case_answers())
        m2m_field_selection = AbnormalFootAppearanceObservations.objects.filter(
            name="infection"
        )

        for foot_choice in self.foot_choices:
            field = f"normal_appearance_{foot_choice}_foot"
            m2m_field = f"abnormal_obs_{foot_choice}_foot"

            with self.subTest(
                f"Testing '{m2m_field}' accepted if {field}='No'",
                field=field,
                m2m_field=m2m_field,
            ):
                cleaned_data.update({field: YES, m2m_field: m2m_field_selection})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertIn(m2m_field, form_validator._errors)
                self.assertIn(
                    "This field is not required",
                    str(form_validator._errors.get(m2m_field)),
                )
                self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

                # Set to No (i.e. make m2m applicable) and move onto next test
                cleaned_data.update({field: NO})

    def test_other_field_required_if_other_specified(self):
        cleaned_data = deepcopy(self.get_best_case_answers())
        other_observation = AbnormalFootAppearanceObservations.objects.filter(name=OTHER)

        for foot_choice in self.foot_choices:
            field = f"normal_appearance_{foot_choice}_foot"
            m2m_field = f"abnormal_obs_{foot_choice}_foot"
            m2m_field_other = f"{m2m_field}_other"

            with self.subTest(
                f"Testing '{m2m_field_other}' required if {m2m_field}={other_observation}",
                field=field,
                m2m_field=m2m_field,
                m2m_field_other=m2m_field_other,
            ):
                # Select 'other', then test it's required
                cleaned_data.update({field: NO, m2m_field: other_observation})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertIn(m2m_field_other, form_validator._errors)
                self.assertIn(
                    "This field is required",
                    str(form_validator._errors.get(m2m_field_other)),
                )
                self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

                # Complete 'other' field, and move onto next test
                cleaned_data.update({m2m_field_other: "Some other value"})

    def test_other_field_not_required_if_other_not_specified(self):
        cleaned_data = self.get_best_case_answers()
        non_other_observation = AbnormalFootAppearanceObservations.objects.filter(
            name="infection"
        )

        for foot_choice in self.foot_choices:
            field = f"normal_appearance_{foot_choice}_foot"
            m2m_field = f"abnormal_obs_{foot_choice}_foot"
            m2m_field_other = f"{m2m_field}_other"

            with self.subTest(
                f"Testing '{m2m_field_other}' completed when not required",
                field=field,
                m2m_field=m2m_field,
                m2m_field_other=m2m_field_other,
            ):
                # Try with normal foot appearance
                cleaned_data.update({field: YES, m2m_field_other: "Some other value"})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertIn(m2m_field_other, form_validator._errors)
                self.assertIn(
                    "This field is not required",
                    str(form_validator._errors.get(m2m_field_other)),
                )
                self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

                # Try with abnormal foot appearance, and non-'other' observation
                cleaned_data.update(
                    {
                        field: NO,
                        m2m_field: non_other_observation,
                        m2m_field_other: "Some other value",
                    }
                )
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertIn(m2m_field_other, form_validator._errors)
                self.assertIn(
                    "This field is not required",
                    str(form_validator._errors.get(m2m_field_other)),
                )
                self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

                # Remove 'other' field value, make valid and move onto next test
                del cleaned_data[m2m_field]
                del cleaned_data[m2m_field_other]
                cleaned_data.update({field: YES})

    def test_missing_required_field_raises_mnsi_patient_history_calculator_error(
        self,
    ):
        cleaned_data = self.get_best_case_answers()
        cleaned_data.pop("numb_legs_feet")

        with self.assertRaises(MnsiPatientHistoryCalculatorError):
            self.validate_form_validator(cleaned_data)

    def test_missing_required_field_raises_mnsi_physical_assessment_calculator_error(
        self,
    ):
        cleaned_data = self.get_best_case_answers()
        cleaned_data.pop("ulceration_left_foot")

        with self.assertRaises(MnsiPhysicalAssessmentCalculatorError):
            self.validate_form_validator(cleaned_data)
