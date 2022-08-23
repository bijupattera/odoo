from odoo import api, fields, models, _


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char('Name', help='Patient Tag', required=True)
    active = fields.Boolean('Active', default=True, copy=False)
    color = fields.Integer('color')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (Copy)") % self.name
        return super(PatientTag, self).copy(default=default)

    _sql_constraints = [
        ('name_uniq', 'unique(name, active)', 'The name already exists and must be unique!'),
        ('color_uniq', 'unique(color)', 'This color is selected already! please choose another.'),
        ('color_check', 'CHECK(color >= 0)', 'The expected number of a color must be nonzero positive.')
    ]