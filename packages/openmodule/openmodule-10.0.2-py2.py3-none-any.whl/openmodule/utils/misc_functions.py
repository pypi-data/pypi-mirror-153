import re


def clean_service_name(name):
    # removing service prefix: "om_"
    cleaned_service_name: str = re.sub(r"^om_", "", name)
    # removing instance suffix: e.g. "_1", "_2"
    cleaned_service_name = re.sub(r"_\d+$", "", cleaned_service_name)
    return cleaned_service_name
