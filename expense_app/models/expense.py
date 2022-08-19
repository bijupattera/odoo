from odoo import api, fields, models


class homedaily(models.Model):
    _name = 'home.daily'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Expense'
    _order = 'date desc'

    # Text fields
    name = fields.Char(
        'Item',
        default=None,
        index=True,
        help='Item bought or expense inccured',
        required=True,
        tracking=True
    )

    notes = fields.Text('Notes', tracking=True)
    descr = fields.Text('Description', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id,
                                 readonly=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    quantity = fields.Integer(default=1, tracking=True)
    amount = fields.Float('Price', required=True, tracking=True )
    total = fields.Monetary('Total', compute="_compute_total", store=True)

    @api.depends('amount', 'quantity')
    def _compute_total(self):
        for record in self:
            record.total = record.quantity * record.amount

    # Date fields
    date = fields.Date(
        'Dated On', tracking=True,
        default=lambda self: fields.Date.today())
    # default=lambda self: fields.Date.today().replace(month=1)) for month of Jan

    # Other fields
    active = fields.Boolean('Active?', default=True)
    post_to_cashinhand = fields.Boolean('Post to Cash In Hand', default=True)
    shop_ids = fields.Many2one('res.partner', string='From Shop', tracking=True)
    category = fields.Selection(
        [('dailyneeds', 'DailyNeeds'),
         ('school', 'School'),
         ('medical', 'Medical'),
         ('maintanance', 'Maintanance'),
         ('dress', 'Dress'),
         ('agriculture', 'Agriculture'),
         ('travel', 'Travel'),
         ('charity', 'Charity')],
        default='dailyneeds', tracking=True
    )

    @api.model
    def create(self, values):
        # update Cash In Hand
        if values['post_to_cashinhand']:
            wt = self.env['cash.inhand']
            wt.create({
                'create_uid': self.env.user.id,
                'date': fields.Datetime.now(),
                'credit': values['quantity'] * values['amount'],
                'debit': 0.00,
                'name': values['name'],
                'notes': "Auto Updated By Model Expanse Create",
            })
            values['post_to_cashinhand'] = False
        return super(homedaily, self).create(values)
