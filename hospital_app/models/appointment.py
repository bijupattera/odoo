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
    age = fields.Integer('Age', compute='_compute_age', default=0)
    prescription = fields.Html('Prescription')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'),
                                 ('3', 'High')], string='Priority')
    state = fields.Selection([('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'),
                              ('canceled', 'Canceled')], string='State', default='draft')


    @api.depends('date_of_birth')
    def _compute_age(self):
        date_today = date.today()
        for rec in self:
            rec.age = date_today.year - rec.date_of_birth.year

    def mark_cancel(self):
        for rec in self:
            rec.state = 'canceled'
            rec.cancel_time = fields.Datetime.now()

