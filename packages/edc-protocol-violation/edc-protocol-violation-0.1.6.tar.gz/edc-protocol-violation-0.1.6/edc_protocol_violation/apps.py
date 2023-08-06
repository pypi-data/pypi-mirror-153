from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "edc_protocol_violation"
    verbose_name = "Edc Protocol Deviations/Violations"
    has_exportable_data = True
    include_in_administration_section = True
