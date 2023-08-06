from odoo_somconnexio_python_client.resources.address import Address


class MobileISPInfo:
    def __init__(
        self,
        type,
        phone_number="",
        previous_provider="",
        previous_owner_vat_number="",
        previous_owner_name="",
        previous_owner_first_name="",
        icc="",
        icc_donor="",
        previous_contract_type="no",
        delivery_address=None,
        invoice_address=None,
    ):
        self.phone_number = phone_number
        self.type = type
        self.previous_provider = previous_provider
        self.previous_owner_vat_number = previous_owner_vat_number
        self.previous_owner_name = previous_owner_name
        self.previous_owner_first_name = previous_owner_first_name
        self.icc = icc
        self.icc_donor = icc_donor
        self.previous_contract_type = previous_contract_type
        if delivery_address:
            self.delivery_address = Address(**delivery_address)
        if invoice_address:
            self.invoice_address = Address(**invoice_address)
