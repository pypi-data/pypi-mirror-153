class Address:
    """
    Address representation.

    More info about the ISO-3166:
    https://en.wikipedia.org/wiki/ISO_3166-2:ES#Provinces

    Attributes:
        street (string): Street name, number and other details.
        street2 (string optional): More details about address.
        zip_code (string): The ZIP code.
        city (string): City name.
        state (string): State code using the ISO-3166.
        country (string): Country code using the ISO-3166.
    """

    def __init__(
        self, street="", zip_code="", city="", state="", country="", street2=None
    ):
        self.street = street
        self.street2 = street2
        self.zip_code = zip_code
        self.city = city
        self.state = state
        self.country = country
