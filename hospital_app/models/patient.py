from datetime import date, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    _order = 'name desc'

    name = fields.Char('Patient Name', help='Patient First Name', required=True, tracking=True)
    last_name = fields.Char('Patient Name', help='Patient First Name', required=True, tracking=True)
    ref = fields.Char('Reference', readonly=True)
    age = fields.Integer('Age', compute='_compute_age')
    image = fields.Image('Image')
    notes = fields.Html('Notes', tracking=True)
    date_of_birth = fields.Date('Date Of Birth', tracking=True, default=lambda self: fields.Date.today())
    active = fields.Boolean('Active?', default=True)
    gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female'),
         ('other', 'Other')], default='female', tracking=True)
    tag_ids = fields.Many2many('patient.tag', string='Tags')

    @api.depends('date_of_birth')
    def _compute_age(self):
        date_today = date.today()
        for rec in self:
            rec.age = date_today.year - rec.date_of_birth.year

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth > fields.Date.today():
                raise ValidationError(_('Entered Date Of Birth is not valid'))

    _sql_constraints = [
        ('name_uniq', 'unique(name, active)', 'The name already exists and must be unique!'),
        ('color_check', 'CHECK(color >= 0)', 'The expected number of a color must be nonzero positive.')
    ]

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    def name_get(self):
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]
