# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    maturity_due_warning = fields.Integer(string='Maturity due warning in days',
                                          config_parameter='expense_app.maturity_due_warning')
