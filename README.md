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

'codeview'=true}" html code <> 

if not self.ref and not vals.get('ref): 

readonly = "1" force_save = "1" to write value to a readonly compute field in field def

many to many check boxe widget

many2one selection widget
_log_access = False

Name create function
    @api.model
    def name_create(self, name):
        return self.create({'appointment_id': name}).name_get()[0]

Hide groups from users form view 
class ResGroups(models.Model):
    _inherit = 'res.groups'

    @api.model
    def get_application_groups(self, domain):
        group2hide = self.env.ref('group_externel_id').id
        return super(ResGroups, self).get_application_groups(domain + [('id', '!=', group2hide)])

Referance Feild 
message_post

Get Metadata
Trim = False fielt def

Active Test
self.env['hospital.patient'].with_context(active_test=False).search_count([]) 

Display Notification with next and url
           return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('The following replenishment order has been generated'),
                    'message': '%s',
                    'links': [{
                        'label': production.name,
                        'url': f'#action={action.id}&id={production.id}&model=home.daily'
                    }],
                    'sticky': False,
                    'next': {'type': 'ir.actions.act_window',
                             'ress_model': '',
                                'res_id': self.id,
                                'views': [[False,'form']]
                    }
                }
            }






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
