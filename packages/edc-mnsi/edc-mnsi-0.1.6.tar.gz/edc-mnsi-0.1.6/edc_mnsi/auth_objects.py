from .utils import get_mnsi_model_name

MNSI = "MNSI"
MNSI_VIEW = "MNSI_VIEW"
MNSI_SUPER = "MNSI_SUPER"

mnsi_codenames = []

app_name, model_name = get_mnsi_model_name().split(".")
for prefix in ["add", "change", "view", "delete"]:
    mnsi_codenames.append(f"{app_name}.{prefix}_{model_name}")
mnsi_codenames.append(f"{app_name}.view_historical{model_name}")
mnsi_codenames.append("edc_mnsi.view_abnormalfootappearanceobservations")
mnsi_codenames.sort()
