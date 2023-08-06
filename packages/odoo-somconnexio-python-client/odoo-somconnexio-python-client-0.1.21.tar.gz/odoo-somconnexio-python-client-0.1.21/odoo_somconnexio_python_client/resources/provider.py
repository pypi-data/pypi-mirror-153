from odoo_somconnexio_python_client.client import Client


class Provider:
    _url_path = "/provider"

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def mobile_list(cls):
        """
        Return a list with all the providers filtered
        by mobile service.

        :return: List of mobile providers
        """
        return cls._get(mobile="true")

    @classmethod
    def broadband_list(cls):
        """
        Return a list with all the providers filtered
        by broadband service.

        :return: List of broadband providers
        """
        return cls._get(broadband="true")

    @classmethod
    def _get(cls, mobile="false", broadband="false"):
        response_data = Client().get(
            "{}".format(cls._url_path),
            params={"mobile": mobile, "broadband": broadband},
        )

        providers = []
        for provider in response_data.get("providers"):
            providers.append(cls(**provider))

        return providers
