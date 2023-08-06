from edc_constants.constants import (
    ABSENT,
    DECREASED,
    NORMAL,
    NOT_EXAMINED,
    PRESENT,
    PRESENT_WITH_REINFORCEMENT,
    REDUCED,
)

ANKLE_REFLEX_CHOICES = (
    (PRESENT, "Present"),
    (PRESENT_WITH_REINFORCEMENT, "Present/Reinforcement"),
    (ABSENT, "Absent"),
    (NOT_EXAMINED, "Not examined"),
)

MONOFILAMENT_CHOICES = (
    (NORMAL, "Normal"),
    (REDUCED, "Reduced"),
    (ABSENT, "Absent"),
    (NOT_EXAMINED, "Not examined"),
)

ULCERATION_CHOICES = (
    (ABSENT, "Absent"),
    (PRESENT, "Present"),
    (NOT_EXAMINED, "Not examined"),
)

VIBRATION_PERCEPTION_CHOICES = (
    (PRESENT, "Present"),
    (DECREASED, "Decreased"),
    (ABSENT, "Absent"),
    (NOT_EXAMINED, "Not examined"),
)
