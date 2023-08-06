from .utils import get_phq9_model_name

PHQ9 = "PHQ9"
PHQ9_VIEW = "PHQ9_VIEW"
PHQ9_SUPER = "PHQ9_SUPER"

phq9_codenames = []

app_name, model_name = get_phq9_model_name().split(".")
for prefix in ["add", "change", "view", "delete"]:
    phq9_codenames.append(f"{app_name}.{prefix}_{model_name}")
phq9_codenames.append(f"{app_name}.view_historical{model_name}")
phq9_codenames.sort()
