from odoo import api, fields, models, _


class HospitalUsers(models.Model):
    _inherit = ['res.users']

    is_doctor = fields.Boolean('Is Doctor?', default="False")
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string='Appointments', readonly='True')
    appointment_count = fields.Integer('Appointment Count', compute='_compute_appointment_count', store=True)

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
