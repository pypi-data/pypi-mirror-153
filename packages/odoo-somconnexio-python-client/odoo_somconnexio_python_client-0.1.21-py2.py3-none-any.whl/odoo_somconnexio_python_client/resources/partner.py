from odoo_somconnexio_python_client.client import Client
from odoo_somconnexio_python_client.resources.address import Address

from ..exceptions import ResourceNotFound


class Partner:
    _url_path = "/partner"

    # TODO: Add all the needed fields in the future...
    def __init__(
        self,
        id,
        name,
        firstname,
        lastname,
        ref,
        lang,
        vat,
        type,
        email,
        phone,
        mobile,
        cooperator_register_number,
        cooperator_end_date,
        coop_agreement_code,
        sponsor_id,
        coop_candidate,
        member,
        sponsorship_code,
        sponsees_max,
        sponsees_number,
        addresses,
        **kwargs
    ):
        self.id = id
        self.name = name
        self.firstname = firstname
        self.lastname = lastname
        self.ref = ref
        self.lang = lang
        self.vat = vat
        self.type = type
        self.email = email
        self.phone = phone
        self.mobile = mobile
        self.cooperator_register_number = cooperator_register_number
        self.cooperator_end_date = cooperator_end_date
        self.sponsor_id = sponsor_id
        self.coop_agreement_code = coop_agreement_code
        self.coop_candidate = coop_candidate
        self.member = member
        self.sponsorship_code = sponsorship_code
        self.sponsees_max = sponsees_max
        self.sponsees_number = sponsees_number
        self.addresses = []
        for address in addresses:
            self.addresses.append(Address(**address))

    @classmethod
    def get(cls, ref):
        """
        Get ResPartner using the ref param.

        :return: Partner object if exists
        """
        return cls._get(id=int(ref))

    @classmethod
    def search_by_vat(cls, vat):
        """
        Search ResPartner in Odoo by VAT number.

        :return: Partner object if exists
        """
        return cls._get(
            params={
                "vat": vat,
            }
        )

    @classmethod
    def check_sponsor(cls, vat, sponsor_code):
        """
        Check if partner can sponsor new partners.

        :return: True or False
        """
        if not vat or not sponsor_code:
            return False

        url = "{}/{}".format(cls._url_path, "check_sponsor")
        params = {
            "vat": vat,
            "sponsor_code": sponsor_code,
        }
        response_data = Client().get(
            url,
            params=params,
        )
        if not response_data:
            raise ResourceNotFound(resource=cls.__name__, filter=params)
        return response_data["result"] == "allowed", response_data["message"]

    @classmethod
    def _get(cls, id=None, params={}):
        if id:
            url = "{}/{}".format(cls._url_path, id)
        else:
            url = cls._url_path

        response_data = Client().get(
            url,
            params=params,
        )
        if not response_data:
            raise ResourceNotFound(resource=cls.__name__, filter=params)

        return cls(**response_data)
