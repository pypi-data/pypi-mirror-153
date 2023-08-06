from edc_list_data.model_mixins import ListModelMixin


class AbnormalFootAppearanceObservations(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Abnormal Foot Appearance Observations"
        verbose_name_plural = "Abnormal Foot Appearance Observations"
