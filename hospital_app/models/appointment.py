from datetime import date
from odoo import api, fields, models


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appointment Record'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patient', 'Patient', tracking=True)
    appointment_time = fields.Datetime('Appointment Date', tracking=True, default=fields.Datetime.now())
    booking_time = fields.Datetime('Time of Booking', tracking=True, readonly=True, default=fields.Datetime.now())
    cancel_time = fields.Datetime('Time of Cancel', tracking=True, readonly=True)
    gender = fields.Selection(related='patient_id.gender')
    date_of_birth = fields.Date(related='patient_id.date_of_birth')
    age = fields.Integer('Age', compute='_compute_age', )
    prescription = fields.Html('Prescription')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'),
                                 ('3', 'High')], string='Priority')
    state = fields.Selection([('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'),
                              ('canceled', 'Canceled')], string='State', default='draft')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')


    @api.depends('date_of_birth')
    def _compute_age(self):
        date_today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = date_today.year - rec.date_of_birth.year
            else:
                rec.age = 1

    def mark_cancel(self):
        for rec in self:
            rec.state = 'canceled'
            rec.cancel_time = fields.Datetime.now()


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', 'Medicine', required=True)
    price = fields.Float(related='product_id.list_price', string='Price')
    qty = fields.Integer('Quantity', default=1)
    total = fields.Float('Total', compute='_compute_total')
    appointment_id = fields.Many2one('hospital.appointment', 'Appointment')

    @api.depends('price', 'qty')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.price * rec.qty
