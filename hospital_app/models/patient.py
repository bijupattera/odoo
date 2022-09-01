from datetime import date, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    _order = 'ref desc'

    name = fields.Char('Patient Name', help='Patient First Name', required=True, tracking=True)
    # last_name = fields.Char('Last Name', help='Patient Last Name', required=True, tracking=True)
    # house_name = fields.Char('House Name', help='Patient House Name', required=True, tracking=True)
    # street = fields.Char('Street', help='Patient Street Name', tracking=True)
    # city = fields.Char('City', help='Patient City', tracking=True)
    # district = fields.Char('District', help='Patient District', required=True, tracking=True)
    # state = fields.Char('State', help='Patient State', required=True, tracking=True)
    # country = fields.Char('Country', help='Patient Country', required=True, tracking=True)
    ref = fields.Char('Reference', readonly=True, search='_search_age')
    age = fields.Integer('Age', compute='_compute_age', search='_search_age', inverse='_inverse_compute_age')
    parent_name = fields.Char('Parent Name', help='Patient Parent Name', tracking=True)
    marital_status = fields.Selection(
        [('married', 'Married'),
         ('single', 'Single'),
         ('other', 'Other')], default='single', tracking=True)
    partner_name = fields.Char('Partner Name', help='Patient Partner Name', tracking=True)
    image = fields.Image('Image')
    notes = fields.Html('Notes', tracking=True)
    date_of_birth = fields.Date('Date Of Birth', tracking=True, default=lambda self: fields.Date.today())
    active = fields.Boolean('Active?', default=True)
    gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female'),
         ('other', 'Other')], default='female', tracking=True, required=True)
    tag_ids = fields.Many2many('patient.tag', string='Tags')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    appointment_count = fields.Integer('Appointment Count', compute='_compute_appointment_count', store=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        date_today = date.today()
        for rec in self:
            rec.age = date_today.year - rec.date_of_birth.year - ((date_today.month,
                                                                   date_today.day) < (rec.date_of_birth.month,
                                                                                      rec.date_of_birth.day))

    def _inverse_compute_age(self):
        date_today = date.today()
        for rec in self:
            rec.date_of_birth = date_today - timedelta(days=(365 * rec.age))

    def _search_age(self, operator, value):
        date_of_birth = date.today() - timedelta(days=(value*365))
        start_of_year = date_of_birth.replace(month=1, day=1)
        end_of_year = date_of_birth.replace(month=12, day=31)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    @api.ondelete(at_uninstall=False)
    def _check_delete(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_('Can not delete Patient with appointments appointment(s)'))

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth > fields.Date.today():
                raise ValidationError(_('Entered Date Of Birth is not valid'))

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    _sql_constraints = [
        ('name_uniq', 'unique(name, active)', 'The name already exists and must be unique!'),
        # ('color_check', 'CHECK(color >= 0)', 'The expected number of a color must be nonzero positive.')
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

    def action_test(self):
        print('clicked groupby button')
        return
