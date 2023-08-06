from edc_protocol_violation.action_items import ProtocolDeviationViolationAction as Base


class ProtocolDeviationViolationAction(Base):

    reference_model = "edc_protocol_violation.protocoldeviationviolation"
    admin_site_name = "edc_protocol_violation"
