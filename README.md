# odoo
Odoo Development projects
Archive
need active field (invisible better) in tree view to get the menu Acrchive

tree or form edit="0", create="0", delete="0" will remove edit, delete, create option in view

Monetory 
price_total = fields.Monetary('Price Total', compute='_sdf_sdf', currency_field='currency_id')
company_id = Fiels.Many2one('Company', 'res.partner', default=lambada self: self.env.user.company)
currency_id = Fields.Many2one('res.currency', related='company_id.currency_id')
if the feild name is not currency_id at py  you can add option currency_field)
view you can add Widget in any field to show the currency symbol

Tracking
can give tracking=1 2, 3 like to get the feilds order in chatter

State/Smart Button
<div class="oe_button_box" name="button_box"> 
	<button class="oe_stat_button" type="object" attrs="{'invisible': ['|', ('sale_order_count', '=', 0), ('type', '=', 'lead')]}"
			name="action_view_hopital.appontment" icon="fa-star">
			<field string="Sales" name="sale_order_count" widget="statinfo"/>
	</button>
</div>

def action_view_hopital.appontment(self):
return {
            'name': name,
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=' 'self.id')],
            'context': {'defaut_patient_id' : self.id},
            'res_model': res_model,
            'view_mode': list,form,delender,activity
            'target': 'current'
            'type' : 'ir.action.act_window'
        }                       
note: use read group method to get the count seach/browse will reduce the performance.
     def _compute_appointment_count(self):
        read_group_data = self.env['hospital.patient'].read_group(domain=[('patient_id', '=', self.id)], fields=['patient_id', grupby=['patient_id'])
        for r in read_group_data:
			patient_id = r.get('patiet_id')[0]
			patient_rec = self.browse(patient_id)
			patient_rec.appointment_count = r['patient_id_count']
			self -= patient_rec  # or  can be write self = self - patient_rec
		self.appointment_count = 0

Widget handle => drag and move teh position
need a field named sequence 
_order = sequense, id  
widget="handle" in field view  

widget many20ne_avatar_user for chat

options="{'collaborative'=Ture}" in field HTML make it collaborative 
default_focus='1'
                          
multi_edit="1"
color and color picker widget 
groups="base.group_no_one" in field def to view the field only in debug mode

RAINBOW MAN 

    def action_set_won_rainbowman(self):
        self.ensure_one()
        self.action_set_won()

        message = self._get_rainbowman_message()
        if message:
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': message,
                    'img_url': '/web/image/%s/%s/image_1024' % (self.team_id.user_id._name, self.team_id.user_id.id) if self.team_id.user_id.image_1024 else '/web/static/img/smile.svg',
                    'type': 'rainbow_man',
                }
            }
        return True
