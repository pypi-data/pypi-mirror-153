from django.contrib import admin

from .fieldsets import get_fieldsets

radio_fields = {
    "amputation": admin.VERTICAL,
    "ankle_reflexes_left_foot": admin.VERTICAL,
    "ankle_reflexes_right_foot": admin.VERTICAL,
    "burning_pain_legs_feet": admin.VERTICAL,
    "covers_touch_skin_painful": admin.VERTICAL,
    "diabetic_neuropathy": admin.VERTICAL,
    "differentiate_hot_cold_water": admin.VERTICAL,
    "feel_weak": admin.VERTICAL,
    "feet_sensitive_touch": admin.VERTICAL,
    "legs_hurt_when_walk": admin.VERTICAL,
    "mnsi_performed": admin.VERTICAL,
    "monofilament_left_foot": admin.VERTICAL,
    "monofilament_right_foot": admin.VERTICAL,
    "muscle_cramps_legs_feet": admin.VERTICAL,
    "normal_appearance_left_foot": admin.VERTICAL,
    "normal_appearance_right_foot": admin.VERTICAL,
    "numb_legs_feet": admin.VERTICAL,
    "open_sore_foot_history": admin.VERTICAL,
    "prickling_feelings_legs_feet": admin.VERTICAL,
    "sense_feet_when_walk": admin.VERTICAL,
    "skin_cracks_open_feet": admin.VERTICAL,
    "symptoms_worse_night": admin.VERTICAL,
    "ulceration_left_foot": admin.VERTICAL,
    "ulceration_right_foot": admin.VERTICAL,
    "vibration_perception_left_toe": admin.VERTICAL,
    "vibration_perception_right_toe": admin.VERTICAL,
}


class MnsiModelAdminMixin:

    form = None

    fieldsets = get_fieldsets()

    filter_horizontal = (
        "abnormal_obs_left_foot",
        "abnormal_obs_right_foot",
    )

    readonly_fields = (
        "calculated_patient_history_score",
        "calculated_physical_assessment_score",
    )

    radio_fields = radio_fields
