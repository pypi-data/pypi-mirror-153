[![pipeline status](https://gitlab.com/coopdevs/odoo-somconnexio-python-client/badges/master/pipeline.svg)](https://gitlab.com/coopdevs/odoo-somconnexio-python-client/commits/master)
[![coverage report](https://gitlab.com/coopdevs/odoo-somconnexio-python-client/badges/master/coverage.svg)](https://gitlab.com/coopdevs/odoo-somconnexio-python-client/commits/master)

:warning: WORK IN PROGRESS :warning:

This library is a Python wrapper for accessing Somconnexio's Odoo (Odoo v12 with customizations).
More info about the customizations in [SomConnexio Odoo module](https://gitlab.com/coopdevs/odoo-somconnexio).

## Resources

* SubscriptionRequest - Customer order
* CRMLead - Service order
* Provider - Service providers
* DiscoveryChannel
* Partner - Customer information

## Installation

```commandline
$ pip install odoo-somconnexio-python-client
```

## Configuration Environment

You need define the Odoo API-KEY and URL as environment variables. You need define:

```
ODOO_BASEURL=<YOUR ODOO HOST>/api
ODOO_APIKEY=<YOUR OC USER>
```

If this envvars are not defined, a exception will be raised with the name of the envvar not defined.
More info about the API-KEY in [Auth API Key](https://github.com/OCA/server-auth/tree/12.0/auth_api_key) Odoo module.

## Usage

#### Search providers by service

```python
>>> from odoo_somconnexio_python_client.resources.provider import Provider
>>>
>>> mobile_providers = Provider.mobile_list()
>>> mobile_providers[0].id
123
>>> mobile_providers[0].name
"SomConnexió"
```

#### Get Partner with ref

```python
>>> from odoo_somconnexio_python_client.resources.partner import Partner
>>>
>>> partner = Partner.get(1234)
>>> partner.id
123
>>> partner.ref
"1234"
```

#### Search Partner by VAT number

```python
>>> from odoo_somconnexio_python_client.resources.partner import Partner
>>>
>>> partner = Partner.search_by_vat(vat="XXXX")
>>> partner.id
123
>>> partner.ref
"1234"
```

### Create new mapper

Create a class that expose a dict objecti with the next structure:

#### Create a SubscriptionRequest

```json
{
  "name": "string",
  "email": "string",
  "ordered_parts": 0,
  "share_product": 0,
  "address": {
    "street": "string",
    "street2": "string",
    "zip_code": "string",
    "city": "string",
    "country": "string",
    "state": "string"
  },
  "lang": "string",
  "iban": "string",
  "vat": "string",
  "coop_agreement": "string",
  "voluntary_contribution": 0,
  "nationality": "string",
  "payment_type": "string"
}
```

#### Create a CRMLead

```json
{
  "iban": "string",
  "subscription_request_id": 0,
  "partner_id": 0,
  "lead_line_ids": [
    {
      "product_code": "string",
      "broadband_isp_info": {
        "phone_number": "string",
        "type": "string",
        "delivery_address": {
          "street": "string",
          "street2": "string",
          "zip_code": "string",
          "city": "string",
          "country": "string",
          "state": "string"
        },
        "previous_provider": 0,
        "previous_owner_vat_number": "string",
        "previous_owner_name": "string",
        "previous_owner_first_name": "string",
        "service_address": {
          "street": "string",
          "street2": "string",
          "zip_code": "string",
          "city": "string",
          "country": "string",
          "state": "string"
        },
        "previous_service": "string",
        "keep_phone_number": true,
        "change_address": true
      },
      "mobile_isp_info": {
        "phone_number": "string",
        "type": "string",
        "delivery_address": {
          "street": "string",
          "street2": "string",
          "zip_code": "string",
          "city": "string",
          "country": "string",
          "state": "string"
        },
        "previous_provider": 0,
        "previous_owner_vat_number": "string",
        "previous_owner_name": "string",
        "previous_owner_first_name": "string",
        "icc": "string",
        "icc_donor": "string",
        "previous_contract_type": "string"
      }
    }
  ]
}
```

## Development

### Setup environment

1. Install `pyenv`
```sh
curl https://pyenv.run | bash
```
2. Build the Python version
```sh
pyenv install  3.8.13
```
3. Create a virtualenv
```sh
pyenv virtualenv 3.8.13 odoo-somconnexio-python-client
```
4. Install dependencies
```sh
pyenv exec pip install -r requirements-dev.txt
```

### Test the HTTP request

We are using the HTTP recording plugin of Pytest: [pytest-recording](https://pytest-vcr.readthedocs.io/).

With VRC we can catch the HTTP responses and then, execute the tests using them.

To add a new test:

* Exepose the needes envvars. Looks the Configuration Environment section
* Execute the tests using `pytest` command:
* If you are writing a new tests that is making requests, you should run:

```
$ pytest --record-mode=once path/to/your/test
```

* You might need to record requests for an specific tests. In that case make sure to only run the tests affected and run

```
$ pytest --record-mode=rewrite path/to/your/test
```

* Add the new `cassetes` to the commit and push them.
* The CI uses the cassetes to emulate the HTTP response in the test.

### Run test suite

```commandline
$ tox
```
### Formatting

We use [Black](https://github.com/psf/black) as formatter.
First to commit, tun the `black` command:

```commandline
$ black .
All done! ✨ 🍰 ✨
29 files left unchanged.
```

### Release process

Update CHANGELOG.md following this steps:

1. Add any entries missing from merged merge requests.
1. Duplicate the `[Unreleased]` header.
1. Replace the second `Unreleased` with a version number followed by the current date. Copy the exact format from previous releases.

Then, you can release and publish the package to PyPi:

1. Update the `VERSION` var in `setup.py` matching the version you specified in the CHANGELOG.
1. Open a merge request with these changes for the team to approve
1. Merge it, add a git tag on that merge commit and push it.
1. Once the pipeline has successfully passed, go approve the `publish` step.
