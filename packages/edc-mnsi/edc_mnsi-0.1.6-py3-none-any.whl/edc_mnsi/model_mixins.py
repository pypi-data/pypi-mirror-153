from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE, YES

from .calculator import MnsiCalculator
from .factory import foot_exam_model_mixin_factory


class MnsiModelMixin(
    foot_exam_model_mixin_factory("right"),
    foot_exam_model_mixin_factory("left"),
    models.Model,
):

    """Neuropathy screening tool.

    Uses Michigan Neuropathy Screening Instrument (MNSI), see:
        https://pubmed.ncbi.nlm.nih.gov/7821168/
        https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3641573/ (omits monofilament testing)
        https://medicine.umich.edu/sites/default/files/downloads/MNSI_howto.pdf

    """

    mnsi_performed = models.CharField(
        verbose_name="Is the MNSI assessment being performed?",
        max_length=15,
        choices=YES_NO,
        default=YES,
        help_text=(
            "If completion of patient history or physical assessment not possible, "
            "respond with `no` and provide reason below."
        ),
    )

    mnsi_not_performed_reason = models.TextField(
        verbose_name="If NO, please provide a reason",
        max_length=200,
        null=True,
        blank=True,
    )

    numb_legs_feet = models.CharField(
        verbose_name="Are your legs and/or feet numb?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    burning_pain_legs_feet = models.CharField(
        verbose_name="Do you ever have any burning pain in your legs and/or feet?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    feet_sensitive_touch = models.CharField(
        verbose_name="Are your feet too sensitive to touch?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    muscle_cramps_legs_feet = models.CharField(
        verbose_name="Do you get muscle cramps in your legs and/or feet?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    prickling_feelings_legs_feet = models.CharField(
        verbose_name="Do you ever have any prickling feelings in your legs or feet?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    covers_touch_skin_painful = models.CharField(
        verbose_name="Does it hurt when the bed covers touch your skin?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    differentiate_hot_cold_water = models.CharField(
        verbose_name=(
            "When you get into the tub or shower, are you able to tell the hot water from the "
            "cold water?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    open_sore_foot_history = models.CharField(
        verbose_name="Have you ever had an open sore on your foot?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    diabetic_neuropathy = models.CharField(
        verbose_name="Has your doctor ever told you that you have diabetic neuropathy?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    feel_weak = models.CharField(
        verbose_name="Do you feel weak all over most of the time?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    symptoms_worse_night = models.CharField(
        verbose_name="Are your symptoms worse at night?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    legs_hurt_when_walk = models.CharField(
        verbose_name="Do your legs hurt when you walk?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    sense_feet_when_walk = models.CharField(
        verbose_name="Are you able to sense your feet when you walk?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    skin_cracks_open_feet = models.CharField(
        verbose_name="Is the skin on your feet so dry that it cracks open?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    amputation = models.CharField(
        verbose_name="Have you ever had an amputation?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    calculated_patient_history_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(13)],
        null=True,
        blank=True,
    )

    calculated_physical_assessment_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10.0)],
        null=True,
        blank=True,
    )

    def update_mnsi_calculated_fields(self) -> None:
        """Calculates the MNSI scores and updates fields.

        Called in a signal.
        """
        mnsi_calculator = MnsiCalculator(model_obj=self)
        self.calculated_patient_history_score = mnsi_calculator.patient_history_score()
        self.calculated_physical_assessment_score = mnsi_calculator.physical_assessment_score()
        self.save(
            update_fields=[
                "calculated_patient_history_score",
                "calculated_physical_assessment_score",
            ]
        )

    class Meta:
        abstract = True
        verbose_name = "Michigan Neuropathy Screening Instrument (MNSI)"
        verbose_name_plural = "Michigan Neuropathy Screening Instrument (MNSI)"
