from django.apps import apps as django_apps

EDC_CSF = "EDC_CSF"
EDC_CSF_SUPER = "EDC_CSF_SUPER"
EDC_CSF_VIEW = "EDC_CSF_VIEW"

codenames = []
app_config = django_apps.get_app_config("edc_csf")
for model_cls in app_config.get_models():
    if "historical" in model_cls._meta.label_lower:
        codenames.append(f"{app_config.name}.view_{model_cls._meta.model_name}")
    else:
        for prefix in ["add", "change", "view", "delete"]:
            codenames.append(f"{app_config.name}.{prefix}_{model_cls._meta.model_name}")
codenames.sort()
