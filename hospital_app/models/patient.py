from datetime import date, timedelta

from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    _order = 'name desc'

    name = fields.Char('Patient Name', help='Patient First Name', required=True, tracking=True)
    ref = fields.Char('Reference')
    age = fields.Integer('Age', compute='_compute_age')
    notes = fields.Html('Notes', tracking=True)
    date_of_birth = fields.Date('Date Of Birth', tracking=True, default=lambda self: fields.Date.today())
    active = fields.Boolean('Active?', default=True)
    gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female'),
         ('other', 'Other')], default='female', tracking=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        date_today = date.today()
        for rec in self:
            rec.age = date_today.year - rec.date_of_birth.year



