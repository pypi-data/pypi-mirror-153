from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

edc_protocol_violation_admin = EdcAdminSite(
    name="edc_protocol_violation_admin", app_label=AppConfig.name
)
