from odoo_somconnexio_python_client.client import Client


class Product:
    def __init__(
        self, name, code, price, category="", minutes="", data="", bandwidth="", available_for=[]
    ):
        self.code = code
        self.name = name
        self.price = price
        self.category = category
        self.minutes = minutes
        self.data = data
        self.bandwidth = bandwidth
        self.available_for = available_for


class ProductCatalog:
    _url_path = "/product-catalog"

    def __init__(self, code, products):
        self.code = code
        self.products = [Product(**product) for product in products]

    @classmethod
    def search(cls, code="", category="", lang="ca", product_code=""):
        headers = {'Accept-Language': lang}
        response_data = Client().get(
            "{}".format(cls._url_path),
            params={"code": code, "categ": category, "product_code": product_code},
            extra_headers=headers
        )

        pricelists = []
        for pricelist in response_data.get("pricelists"):
            pricelists.append(cls(**pricelist))

        return pricelists
