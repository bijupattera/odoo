from datetime import datetime

from odoo import api, fields, models


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment'
    _description = 'Cancel Appointment Wizard'
    
    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['cancel_time'] = datetime.now()
        # if not self.env.context.get('active_id'):
        #     res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment',
                                     help='Cancel Appointment Wizard', required=True)
    reason = fields.Text('Reason')
    cancel_time = fields.Datetime('Cancel Time')

    def action_cancel_appointment(self):
        return

