from odoo import http
from odoo.http import Root
from odoo.http import request
from .http import HttpRestRequest
from odoo.addons.somconnexio.services import (
    contract_contract_service, contract_iban_change_service,
    contract_one_shot_service, contract_change_tariff_service,
    partner_email_change_service, contract_email_change_service
)


class UserPublicController(http.Controller):

    @http.route(['/public-api/contract'], auth='public',
                methods=['POST'], csrf=False)
    def create_contract(self, **kwargs):
        service = contract_contract_service.ContractService(request.env)
        data = request.params
        response = service.create(**data)
        return request.make_json_response(response)

    @http.route(['/public-api/contract-iban-change'], auth='public',
                methods=['POST'], csrf=False)
    def run_contract_iban_change(self, **kwargs):
        service = contract_iban_change_service.ContractIbanChangeService(request.env)
        data = request.params
        response = service.run_from_api(**data)
        return request.make_json_response(response)

    @http.route(['/public-api/partner-email-change'], auth='public',
                methods=['POST'], csrf=False)
    def run_partner_email_change(self, **kwargs):
        service = partner_email_change_service.PartnerEmailChangeService(request.env)
        data = request.params
        response = service.run_from_api(**data)
        return request.make_json_response(response)

    @http.route(['/public-api/contract-email-change'], auth='public',
                methods=['POST'], csrf=False)
    def run_contract_email_change(self, **kwargs):
        service = contract_email_change_service.PartnerEmailChangeService(request.env)
        data = request.params
        response = service.run_from_api(**data)
        return request.make_json_response(response)

    @http.route(['/public-api/contract-count'], auth='public',
                methods=['GET'], csrf=False)
    def count_contract(self):
        service = contract_contract_service.ContractService(request.env)
        response = service.count()
        return request.make_json_response(response)

    @http.route(['/public-api/add-one-shot'], auth='public',
                methods=['POST'], csrf=False)
    def run_add_contract_one_shot(self, **kwargs):
        service = contract_one_shot_service.ContractOneShotAdditionService(request.env)
        data = request.params
        response = service.run_from_api(**data)
        return request.make_json_response(response)

    @http.route(['/public-api/change-tariff'], auth='public',
                methods=['POST'], csrf=False)
    def run_change_contract_tariff(self, **kwargs):
        service = contract_change_tariff_service.ContractChangeTariffService(
            request.env)
        data = request.params
        response = service.run_from_api(**data)
        return request.make_json_response(response)


ori_get_request = Root.get_request


def get_request(self, httprequest):
    if (
            httprequest.path.startswith('/public-api/contract') or
            httprequest.path.startswith('/public-api/add-one-shot') or
            httprequest.path.startswith('/public-api/change-tariff') or
            httprequest.path.startswith('/public-api/partner-email-change')
    ):
        return HttpRestRequest(httprequest)
    return ori_get_request(self, httprequest)


Root.get_request = get_request
