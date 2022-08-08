from odoo import api, fields, models

class varumanam(models.Model):
    _name = 'varu.manam'
    _description = 'Income'
    _order = 'date desc'

    # Text fields
    name = fields.Char(
        'Item',
        default=None,
        index=True,
        help='Income source',
        readonly=False,
        required=True,
        translate=False,
    )

    notes = fields.Text('Notes')
    descr = fields.Text('Description')

    # Numeric fields
    quantity = fields.Integer(default=1)
    amount = fields.Monetary('Price ₹')
    total = fields.Monetary('Total ₹', compute="_compute_total", store=True)
    
    @api.depends("amount")
    def _compute_total(self):
        for record in self:
            record.total = record.quantity * record.amount

    # Date fields
    date = fields.Date(
        'Dated On',
        default=lambda self: fields.Date.today())
        # default=lambda self: fields.Date.today().replace(month=1)) for month of Jan

    # Other fields
    active = fields.Boolean('Active?', default=True)

    # Relational fields
    shop_ids = fields.Many2many('res.partner', string='From Shop')
    
    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True
    )
    
    category = fields.Selection(
        [('coconut','Coconut'),
         ('support','Support'),
         ('aricanut','Arikanut'),
         ('interest','Interest'),
         ('property','RealEstate'),
         ('others','Others')],
        default='coconut',
    )