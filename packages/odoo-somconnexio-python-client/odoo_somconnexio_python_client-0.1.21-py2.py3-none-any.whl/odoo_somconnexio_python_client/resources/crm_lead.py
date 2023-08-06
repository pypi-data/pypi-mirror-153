from odoo_somconnexio_python_client.resources.crm_lead_line import CRMLeadLine
from odoo_somconnexio_python_client.client import Client


class CRMLead:
    _name = "crm_lead"
    _url_path = "/crm-lead"

    def __init__(
        self,
        id,
        iban=None,
        lead_line_ids=None,
        subscription_request_id=None,
        partner_id=None,
    ):
        lead_lines = []
        if lead_line_ids:
            for lead_line in lead_line_ids:
                lead_lines.append(CRMLeadLine(**lead_line))

        self.id = id
        self.lead_line_ids = lead_lines
        self.iban = iban
        self.partner_id = partner_id
        self.subscription_request_id = subscription_request_id

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a CRMLead instance.

        :param kwargs:
        :return:
        """
        response_data = Client().post("{}/create".format(cls._url_path), kwargs)

        return cls(**response_data)
