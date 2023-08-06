from edc_constants.constants import NO, NOT_EXAMINED, OTHER, YES
from edc_form_validators import FormValidator

from .calculator import MnsiCalculator
from .fieldsets import patient_history_fields


class MnsiFormValidator(FormValidator):
    def clean(self):
        self.required_if(
            NO,
            field="mnsi_performed",
            field_required="mnsi_not_performed_reason",
        )
        self.clean_patient_history_fields()
        self.clean_physical_assessments()
        self.clean_calculation_data()

    def clean_patient_history_fields(self):
        for field in patient_history_fields:
            self.applicable_if(
                YES,
                field="mnsi_performed",
                field_applicable=field,
            )

    def foot_amputated(self, foot_choice: str) -> bool:
        if self.cleaned_data.get(
            f"normal_appearance_{foot_choice}_foot"
        ) == NO and self.cleaned_data.get(f"abnormal_obs_{foot_choice}_foot"):
            qs = self.cleaned_data.get(f"abnormal_obs_{foot_choice}_foot")
            return qs.filter(name="deformity_amputation").exists()
        return False

    def clean_physical_assessments(self):
        applicable_if_opts = dict(
            not_applicable_value=NOT_EXAMINED,
            applicable_msg=(
                "Invalid. Examination result expected if MNSI assessment was performed."
            ),
            not_applicable_msg=(
                "Invalid. Expected `not examined` if MNSI assessment was not performed.",
            ),
        )
        for foot_choice in ["right", "left"]:

            self.applicable_if(
                YES,
                field="mnsi_performed",
                field_applicable=f"normal_appearance_{foot_choice}_foot",
                **applicable_if_opts,
            )

            self.m2m_required_if(
                response=NO,
                field=f"normal_appearance_{foot_choice}_foot",
                m2m_field=f"abnormal_obs_{foot_choice}_foot",
            )

            self.m2m_other_specify(
                OTHER,
                m2m_field=f"abnormal_obs_{foot_choice}_foot",
                field_other=f"abnormal_obs_{foot_choice}_foot_other",
            )

            for target_field in [
                f"ulceration_{foot_choice}_foot",
                f"ankle_reflexes_{foot_choice}_foot",
                f"vibration_perception_{foot_choice}_toe",
                f"monofilament_{foot_choice}_foot",
            ]:

                if not self.foot_amputated(foot_choice):
                    self.applicable_if(
                        YES,
                        field="mnsi_performed",
                        field_applicable=target_field,
                        **applicable_if_opts,
                    )

    def clean_calculation_data(self):
        mnsi_calculator = MnsiCalculator(**self.cleaned_data)
        mnsi_calculator.patient_history_score()
        mnsi_calculator.physical_assessment_score()
