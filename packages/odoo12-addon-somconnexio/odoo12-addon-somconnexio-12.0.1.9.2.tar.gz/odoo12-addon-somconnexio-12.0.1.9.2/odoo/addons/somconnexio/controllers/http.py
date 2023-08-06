from odoo.addons.base_rest.http import HttpRestRequest
import json
import logging

_logger = logging.getLogger(__name__)
try:
    import pyquerystring
except (ImportError, IOError) as err:
    _logger.debug(err)


class HttpRestRequest(HttpRestRequest):
    """Http request that always return json, usefull for rest api"""

    def __init__(self, httprequest):
        super(HttpRestRequest, self).__init__(httprequest)
        if self.httprequest.mimetype != "application/json":
            data = self.httprequest.data.decode(self.httprequest.charset)
            data_dec = pyquerystring.parse(data)
            if 'body' in data_dec:
                self.params = json.loads(data_dec['body'])
