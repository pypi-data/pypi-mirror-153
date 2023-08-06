calculated_values_fieldset = (
    "Calculated values",
    {
        "classes": ("collapse",),
        "fields": (
            "calculated_patient_history_score",
            "calculated_physical_assessment_score",
        ),
    },
)

patient_history_fields = (
    "numb_legs_feet",
    "burning_pain_legs_feet",
    "feet_sensitive_touch",
    "muscle_cramps_legs_feet",
    "prickling_feelings_legs_feet",
    "covers_touch_skin_painful",
    "differentiate_hot_cold_water",
    "open_sore_foot_history",
    "diabetic_neuropathy",
    "feel_weak",
    "symptoms_worse_night",
    "legs_hurt_when_walk",
    "sense_feet_when_walk",
    "skin_cracks_open_feet",
    "amputation",
)


def get_physical_assessment_fields(foot_choice):
    return (
        f"normal_appearance_{foot_choice}_foot",
        f"abnormal_obs_{foot_choice}_foot",
        f"abnormal_obs_{foot_choice}_foot_other",
        f"ulceration_{foot_choice}_foot",
        f"ankle_reflexes_{foot_choice}_foot",
        f"vibration_perception_{foot_choice}_toe",
        f"monofilament_{foot_choice}_foot",
    )


def get_fieldsets():
    return (
        (
            "Part 1: Patient History",
            {
                "description": (
                    "To be completed by the patient. If the MNSI assessment "
                    "was not performed, the response is `not applicable`."
                ),
                "fields": patient_history_fields,
            },
        ),
        (
            "Part 2a: Physical Assessment - Right Foot",
            {
                "description": "To be completed by health professional",
                "fields": get_physical_assessment_fields("right"),
            },
        ),
        (
            "Part 2b: Physical Assessment - Left Foot",
            {
                "description": "To be completed by health professional",
                "fields": get_physical_assessment_fields("left"),
            },
        ),
    )
