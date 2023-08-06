from edc_auth.auth_objects import AUDITOR_ROLE, CLINICIAN_ROLE, CLINICIAN_SUPER_ROLE
from edc_auth.site_auths import site_auths
from edc_data_manager.auth_objects import DATA_MANAGER_ROLE

from edc_protocol_violation.auth_objects import (
    PROTOCOL_VIOLATION,
    PROTOCOL_VIOLATION_VIEW,
    protocol_violation_codenames,
    protocol_violation_view_codenames,
)

site_auths.add_group(*protocol_violation_codenames, name=PROTOCOL_VIOLATION)
site_auths.add_group(*protocol_violation_view_codenames, name=PROTOCOL_VIOLATION_VIEW)
site_auths.update_role(PROTOCOL_VIOLATION, name=CLINICIAN_ROLE)
site_auths.update_role(PROTOCOL_VIOLATION, name=CLINICIAN_SUPER_ROLE)
site_auths.update_role(PROTOCOL_VIOLATION, name=DATA_MANAGER_ROLE)
site_auths.update_role(PROTOCOL_VIOLATION_VIEW, name=AUDITOR_ROLE)
