from datetime import date, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appointment Record'
    _rec_name = 'ref'

    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        #if not self.env.context.get('default_patient_id'):
        res['patient_id'] = self.env.context.get('default_patient_id')
        return res

    appointment_id = fields.Char('Appointment ID', readonly=True)
    active = fields.Boolean('Active', default=True)
    patient_id = fields.Many2one('hospital.patient', 'Patient', tracking=True, required=True)
    ref = fields.Char('Reference', readonly=True)
    appointment_time = fields.Datetime('Appointment Date', tracking=True, default=fields.Datetime.now())
    booking_time = fields.Datetime('Time of Booking', tracking=True, readonly=True, default=fields.Datetime.now())
    cancel_time = fields.Datetime('Time of Cancel', tracking=True, readonly=True)
    gender = fields.Selection(related='patient_id.gender', search='_search_gender')
    date_of_birth = fields.Date(related='patient_id.date_of_birth')
    age = fields.Integer('Age', compute='_compute_age', search='_search_age')
    prescription = fields.Html('Prescription')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'),
                                 ('3', 'High')], string='Priority')
    state = fields.Selection([('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'),
                              ('canceled', 'Canceled')], string='State')
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')


    @api.depends('date_of_birth')
    def _compute_age(self):
        date_today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = date_today.year - rec.date_of_birth.year
            else:
                rec.age = 1

    def _search_age(self, operator, value):
        date_of_birth = date.today() - timedelta(days=(value * 365))
        start_of_year = date_of_birth.replace(month=1, day=1)
        end_of_year = date_of_birth.replace(month=12, day=31)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    def _search_gender(self, operator, value):
        gender = self.env['hospital.patient'].search[('patient_id.id', '=' 'r.id').gender]
        return [gender]

    def action_cancel(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("You can cancel Records in Draft state only"))
            rec.state = 'canceled'
            rec.cancel_time = fields.Datetime.now()
            rec.active = False

    def action_done(self):
        for rec in self:
            if rec.state != 'in_consultation':
                raise ValidationError(_("Record not in a state to mark as Done"))
            rec.state = 'done'

    def mark_cancel(self):
        action = self.env.ref('hospital_app.action_cancel_appointment').read()[0]
        return action

    def set_sl_numbers(self):
        sl_no = 0
        for line in self.pharmacy_line_ids:
            sl_no += 1
            line.sl_no = sl_no
        return

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        vals['state'] = 'draft'
        res = super(HospitalAppointment, self).create(vals)
        res.set_sl_numbers()
        print(self.env.context)
        return res

    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        self.set_sl_numbers()
        return res

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("You can delete Records in Draft state only"))
        return super(HospitalAppointment, self).unlink()


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'
    _rec_name = 'product_id'

    sl_no = fields.Integer('SL NO')
    product_id = fields.Many2one('product.product', 'Medicine', required=True)
    price = fields.Float(related='product_id.list_price', string='Price')
    qty = fields.Integer('Quantity', default=1)
    total = fields.Float('Total', compute='_compute_total')
    appointment_id = fields.Many2one('hospital.appointment', 'Appointment')

    @api.depends('price', 'qty')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.price * rec.qty
