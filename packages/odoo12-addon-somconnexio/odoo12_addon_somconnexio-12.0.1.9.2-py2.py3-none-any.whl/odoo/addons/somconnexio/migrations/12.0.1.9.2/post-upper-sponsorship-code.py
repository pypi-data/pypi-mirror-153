from odoo import SUPERUSER_ID, api

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("Set sponsorship hash to upper")  # noqa
    partners = env["res.partner"].search([
        '|', ('coop_candidate', '=', True), ('member', '=', True)]
    )
    partners._compute_sponsorship_hash()
    for partner in partners:
        partner.sponsorship_hash = partner.sponsorship_hash.upper()
    _logger.info("Set sponsorship hash to upper ends")
