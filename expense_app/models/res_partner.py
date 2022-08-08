from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    grocery = fields.Boolean('Grocery?', default=True)
