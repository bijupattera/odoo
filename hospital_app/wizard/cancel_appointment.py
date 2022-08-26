from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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
                                     domain=[('state', '=', 'draft'), ('priority', 'in', ('1', '0', False))],
                                     help='Cancel Appointment Wizard', required=True)
    reason = fields.Text('Reason')
    cancel_time = fields.Datetime('Cancel Time')

    def action_cancel_appointment(self):
        if self.appointment_id.appointment_time < (fields.Datetime.now() + timedelta(days=1)):
            raise ValidationError(_("Sorry, Appointment cancellation is allowed minimum of one day before"))
        self.appointment_id.state = 'canceled'


