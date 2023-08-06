from odoo_somconnexio_python_client.resources.broadband_isp_info import BroadbandISPInfo
from odoo_somconnexio_python_client.resources.mobile_isp_info import MobileISPInfo


class CRMLeadLine:
    def __init__(self, product_code, broadband_isp_info=None, mobile_isp_info=None):
        self.product_code = product_code
        if broadband_isp_info:
            self.broadband_isp_info = BroadbandISPInfo(**broadband_isp_info)
        if mobile_isp_info:
            self.mobile_isp_info = MobileISPInfo(**mobile_isp_info)
