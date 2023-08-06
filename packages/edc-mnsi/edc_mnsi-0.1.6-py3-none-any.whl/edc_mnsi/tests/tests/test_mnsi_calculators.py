from django.test import TestCase
from edc_constants.constants import (
    ABSENT,
    DECREASED,
    NO,
    NOT_EXAMINED,
    PRESENT,
    PRESENT_WITH_REINFORCEMENT,
    REDUCED,
    YES,
)

from edc_mnsi.calculator import (
    MnsiCalculator,
    MnsiPatientHistoryCalculatorError,
    MnsiPhysicalAssessmentCalculatorError,
)

from .mixins import TestCaseMixin


class TestMnsiCalculators(TestCaseMixin, TestCase):
    def test_calculator_instantiated_with_dict(self):
        responses = self.get_best_case_answers()
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 0)

    def test_calculator_instantiated_with_model(self):
        responses = self.get_best_case_answers()
        model = self.get_mnsi_obj(**responses)
        mnsi_calculator = MnsiCalculator(model)
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 0)

    def test_calculator_instantiated_with_dict2(self):
        responses = self.get_best_case_answers()
        responses.update(self.get_worst_case_patient_history_data())
        responses.update(self.get_worst_case_physical_assessment_data())
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 13)
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 10)

    def test_calculator_instantiated_with_model2(self):
        responses = self.get_best_case_answers()
        responses.update(self.get_worst_case_patient_history_data())
        responses.update(self.get_worst_case_physical_assessment_data())
        model = self.get_mnsi_obj(**responses)
        mnsi_calculator = MnsiCalculator(model)
        self.assertEqual(mnsi_calculator.patient_history_score(), 13)
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 10)

    def test_calculator_instantiated_with_dict_when_mnsi_not_performed(self):
        responses = self.get_mnsi_not_performed_answers()
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 0)

    def test_calculator_instantiated_with_model_when_mnsi_not_performed(self):
        responses = self.get_mnsi_not_performed_answers()
        model = self.get_mnsi_obj(**responses)
        mnsi_calculator = MnsiCalculator(model)
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 0)

    def test_missing_required_field_raises_mnsi_patient_history_calculator_error(
        self,
    ):
        responses = self.get_best_case_answers()
        responses.pop("amputation")
        mnsi_calculator = MnsiCalculator(**responses)
        with self.assertRaises(MnsiPatientHistoryCalculatorError):
            mnsi_calculator.patient_history_score()

    def test_missing_non_required_fields_does_not_raise_mnsi_patient_history_calculator_error(
        self,
    ):
        responses = self.get_best_case_answers()
        responses.pop("muscle_cramps_legs_feet")
        responses.pop("feel_weak")
        mnsi_calculator = MnsiCalculator(**responses)
        try:
            mnsi_calculator.patient_history_score()
        except MnsiPatientHistoryCalculatorError as exc:
            self.fail(
                f"mnsi_calculator.patient_history_score() raised "
                f"MnsiPatientHistoryCalculatorError unexpectedly.\nDetails: {exc}"
            )

    def test_missing_required_field_raises_mnsi_physical_assessment_calculator_error(
        self,
    ):
        responses = self.get_best_case_answers()
        responses.pop("ulceration_left_foot")
        mnsi_calculator = MnsiCalculator(**responses)
        with self.assertRaises(MnsiPhysicalAssessmentCalculatorError):
            mnsi_calculator.physical_assessment_score()

    def test_best_case_patient_history_returns_min_score_of_zero(self):
        mnsi_calculator = MnsiCalculator(**self.get_best_case_answers())
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)

    def test_patient_history_returns_score_of_zero_when_mnsi_not_performed(self):
        mnsi_calculator = MnsiCalculator(**self.get_mnsi_not_performed_answers())
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)

    def test_worst_case_patient_history_returns_max_score_of_thirteen(self):
        responses = self.get_best_case_answers()
        responses.update(self.get_worst_case_patient_history_data())
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 13)

    def test_q4_and_q10_do_not_affect_patient_history_score(self):
        # Best case score should be 0
        responses = self.get_best_case_answers()
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)

        # Best case score should remain 0 after modifying q4 and 10
        responses.update({"muscle_cramps_legs_feet": YES, "feel_weak": YES})
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)

        # Worst case score should be 13
        responses.update(self.get_worst_case_patient_history_data())
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 13)

        # Best case score should remain 13 after modifying q4 and 10
        responses.update({"muscle_cramps_legs_feet": NO, "feel_weak": NO})
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 13)

    def test_best_case_physical_assessment_returns_min_score_of_zero(self):
        mnsi_calculator = MnsiCalculator(**self.get_best_case_answers())
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 0)

    def test_physical_assessment_returns_score_of_zero_when_mnsi_not_performed(self):
        mnsi_calculator = MnsiCalculator(**self.get_mnsi_not_performed_answers())
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 0)

    def test_worst_case_physical_assessment_returns_max_score_of_ten(self):
        responses = self.get_best_case_answers()
        responses.update(self.get_worst_case_physical_assessment_data())
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 10)

    def test_patient_history_scores_where_YES_awards_one_point(self):
        one_point_if_yes_response_questions = [
            "numb_legs_feet",  # Q1
            "burning_pain_legs_feet",  # Q2
            "feet_sensitive_touch",  # Q3
            "prickling_feelings_legs_feet",  # Q5
            "covers_touch_skin_painful",  # Q6
            "open_sore_foot_history",  # Q8
            "diabetic_neuropathy",  # Q9
            "symptoms_worse_night",  # Q11
            "legs_hurt_when_walk",  # Q12
            "skin_cracks_open_feet",  # Q14
            "amputation",  # Q15
        ]

        for question in one_point_if_yes_response_questions:
            with self.subTest(
                f"Testing '{question}' with 'YES' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = YES
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.patient_history_score(), 1)

    def test_patient_history_scores_where_NO_awards_one_point(self):
        one_point_if_no_response_questions = [
            "differentiate_hot_cold_water",  # Q7
            "sense_feet_when_walk",  # Q13
        ]

        for question in one_point_if_no_response_questions:
            with self.subTest(
                f"Testing '{question}' with 'NO' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = NO
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.patient_history_score(), 1)

    def test_physical_assessment_abnormal_foot_appearance_awards_one_point(self):
        normal_foot_appearance_questions = [
            "normal_appearance_right_foot",
            "normal_appearance_left_foot",
        ]

        for question in normal_foot_appearance_questions:
            with self.subTest(
                f"Testing '{question}' with 'NO' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = NO
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 1.0)

    def test_physical_assessment_amputation_with_no_further_examinations_awards_one_point(
        self,
    ):
        for foot_choice in self.foot_choices:
            for amputated_obs_set in self.amputated_abnormal_obs_sets:
                with self.subTest(
                    (
                        f"Testing '{foot_choice}' amputated with no further "
                        "examinations is worth 1 point"
                    ),
                    foot_choice=foot_choice,
                    abnormal_obs=amputated_obs_set,
                ):
                    responses = self.get_best_case_answers()
                    responses.update(
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

                    mnsi_calculator = MnsiCalculator(**responses)
                    self.assertEqual(mnsi_calculator.physical_assessment_score(), 1.0)

    def test_physical_assessment_foot_ulceration_present_awards_one_point(self):
        ulceration_questions = [
            "ulceration_right_foot",
            "ulceration_left_foot",
        ]

        for question in ulceration_questions:
            with self.subTest(
                f"Testing '{question}' with 'PRESENT' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = PRESENT
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 1.0)

    def test_physical_assessment_ankle_reflexes_present_reinforcement_awards_half_point(
        self,
    ):
        ankle_reflex_questions = [
            "ankle_reflexes_right_foot",
            "ankle_reflexes_left_foot",
        ]

        for question in ankle_reflex_questions:
            with self.subTest(
                f"Testing '{question}' with 'PRESENT_REINFORCEMENT' response "
                "is worth 0.5 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = PRESENT_WITH_REINFORCEMENT
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 0.5)

    def test_physical_assessment_ankle_reflexes_absent_awards_one_point(
        self,
    ):
        ankle_reflex_questions = [
            "ankle_reflexes_right_foot",
            "ankle_reflexes_left_foot",
        ]

        for question in ankle_reflex_questions:
            with self.subTest(
                f"Testing '{question}' with 'ABSENT' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = ABSENT
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 1)

    def test_physical_assessment_vibration_perception_decreased_awards_half_point(
        self,
    ):
        vibration_perception_questions = [
            "vibration_perception_right_toe",
            "vibration_perception_left_toe",
        ]

        for question in vibration_perception_questions:
            with self.subTest(
                f"Testing '{question}' with 'DECREASED' response is worth 0.5 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = DECREASED
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 0.5)

    def test_physical_assessment_vibration_perception_absent_awards_one_point(
        self,
    ):
        vibration_perception_questions = [
            "vibration_perception_right_toe",
            "vibration_perception_left_toe",
        ]

        for question in vibration_perception_questions:
            with self.subTest(
                f"Testing '{question}' with 'ABSENT' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = ABSENT
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 1)

    def test_physical_assessment_monofilament_reduced_awards_half_point(
        self,
    ):
        monofilament_questions = [
            "monofilament_right_foot",
            "monofilament_left_foot",
        ]

        for question in monofilament_questions:
            with self.subTest(
                f"Testing '{question}' with 'REDUCED' response is worth 0.5 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = REDUCED
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 0.5)

    def test_physical_assessment_monofilament_absent_awards_one_point(
        self,
    ):
        monofilament_questions = [
            "monofilament_right_foot",
            "monofilament_left_foot",
        ]

        for question in monofilament_questions:
            with self.subTest(
                f"Testing '{question}' with 'ABSENT' response is worth 0.5 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = ABSENT
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 1)
