from odoo_somconnexio_python_client.resources.address import Address
from odoo_somconnexio_python_client.client import Client


class SubscriptionRequest:
    _name = "subscription_request"
    _url_path = "/subscription-request"

    def __init__(
        self,
        id=0,
        name="",
        # TODO: Falta en la API
        surname="",
        email="",
        ordered_parts="",
        address="",
        lang="",
        share_product="",
        iban="",
        vat="",
        coop_agreement=0,
        nationality=0,
        payment_type="",
        voluntary_contribution="",
        **kwargs
    ):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.ordered_parts = ordered_parts
        self.address = Address(**address)
        self.lang = lang
        self.share_product = share_product
        self.iban = iban
        self.vat = vat
        self.coop_agreement = coop_agreement
        self.nationality = nationality
        self.payment_type = payment_type
        self.voluntary_contribution = voluntary_contribution

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a SubscriptionRequest instance.

        :param kwargs:
        :return:
        """
        response_data = Client().post("{}/create".format(cls._url_path), kwargs)

        return cls(**response_data)
