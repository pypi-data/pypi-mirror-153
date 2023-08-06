from odoo_somconnexio_python_client.resources.address import Address


class BroadbandISPInfo:
    def __init__(
        self,
        type,
        service_address,
        phone_number="",
        previous_provider="",
        previous_owner_vat_number="",
        previous_owner_name="",
        previous_owner_first_name="",
        previous_service="",
        keep_phone_number="",
        change_address="no",
        delivery_address=None,
        invoice_address=None,
    ):
        self.phone_number = phone_number
        self.type = type
        self.previous_provider = previous_provider
        self.previous_owner_vat_number = previous_owner_vat_number
        self.previous_owner_name = previous_owner_name
        self.previous_owner_first_name = previous_owner_first_name
        self.previous_service = previous_service
        self.keep_phone_number = keep_phone_number
        self.change_address = change_address
        self.service_address = Address(**service_address)
        if delivery_address:
            self.delivery_address = Address(**delivery_address)
        if invoice_address:
            self.invoice_address = Address(**invoice_address)
