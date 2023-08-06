from django.apps import apps as django_apps

EDC_MICROBIOLOGY = "EDC_MICROBIOLOGY"
EDC_MICROBIOLOGY_SUPER = "EDC_MICROBIOLOGY_SUPER"
EDC_MICROBIOLOGY_VIEW = "EDC_MICROBIOLOGY_VIEW"

codenames = []
app_config = django_apps.get_app_config("edc_microbiology")
for model_cls in app_config.get_models():
    if "historical" in model_cls._meta.label_lower:
        codenames.append(f"{app_config.name}.view_{model_cls._meta.model_name}")
    else:
        for prefix in ["add", "change", "view", "delete"]:
            codenames.append(f"{app_config.name}.{prefix}_{model_cls._meta.model_name}")
codenames.sort()
