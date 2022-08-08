from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class sip(models.Model):
    _name = 'sip.invest'
    _description = 'Sip Investment Tracker'
    _order = 'date desc'

    name = fields.Char(
        'Mutual Fund',
        default=None,
        index=True,
        help='Mutual Fund name',
        readonly=False,
        required=True,
        translate=False,
    )

    notes = fields.Text('Notes')
    descr = fields.Text('Description')
    
    invested = fields.Monetary('Amount Invested ₹')
    
    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True
    )
    
    gain = fields.Monetary('Gain ₹', compute="_compute_gain", store=True)
    quantity = fields.Float('Number of Units', default=1)
    amount = fields.Monetary('NAV ₹', compute="_compute_nav", store=True)
    total = fields.Monetary('Now ₹')
    gain_percent = fields.Integer('%', compute="_compute_gain_percent", store=True)
    
    @api.depends("total", "quantity")
    def _compute_nav(self):
        for record in self:
            record.amount = record.total / record.quantity
            
    @api.depends("invested", "total")
    def _compute_gain(self):
        for record in self:
            record.gain = record.total - record.invested
            if record.gain > 0:
                record.stage_id = 'gain'
            elif record.gain < 0:
                record.stage_id = 'loss'
            elif record.gain == '0.00':
                record.stage_id = 'new'
        
            
    @api.depends("invested", "gain")
    def _compute_gain_percent(self):
        for record in self:
            record.gain_percent = record.gain / record.invested * 100
 
    date = fields.Date(
        'Dated On',
        default=lambda self: fields.Date.today())
        # default=lambda self: fields.Date.today().replace(month=1)) for month of Jan

    active = fields.Boolean('Active?', default=True)

    broker_ids = fields.Many2many('res.partner', string='From Broker')
    
    category = fields.Selection(
        [('mid','Mid Cap'),
         ('multicap','Multi Cap'),
         ('small','Small Cap'),
         ('large','Large Cap')],
        default='mid',
    )

    state = fields.Selection(
        [('open','Open'),
         ('clossed','Clossed')],
        default='open',
    )
    
    def button_close(self):
        clossed_stage = 'clossed'
        for c in self:
            c.stage_id = clossed_stage
            c.state = clossed_stage
            c.active = 'False'
        return True
        
    
    stage_id = fields.Selection(
        [('new','No Gain/Loss'),
         ('gain','Gain'),
         ('loss','Loss'),
         ('clossed','Clossed')],
        default='new',
    )

    @api.model
    def create(self, vals):
        sipname = vals['name']
        wt = self.env['fd.invest']
        fdid = wt.search([('name', '=', sipname), ("category", 'ilike', 'SIP')]).id
        print('Updating Assets SIP  ' + sipname + ' ID:' + str(fdid))
        wt.browse(fdid).write({
            'create_uid': self.env.user.id,
            'date': vals['date'],
            'value': vals['total'],
            'invested': vals['invested'],
            'notes': "Auto Updated By Model SIP.INVEST Create",
        })
        res = super(sip, self).create(vals)
        return res

    def write(self, vals):
        today = date.today()
        if today.month != self.date.month or today.year != self.date.year:
            raise UserError(_('You can not UPDATE a record other than this month'))
        else:
            vals['date'] = today
            res = super(sip, self).write(vals)
            sipname = self.name
            wt = self.env['fd.invest']
            fdid = wt.search([('name', '=', sipname), ("category", 'ilike', 'SIP')]).id
            wt.browse(fdid).write({
                'create_uid': self.env.user.id,
                'date': date.today(),
                'value': self.total,
                'invested': self.invested,
                'notes': "Auto Updated By Model SIP.INVEST Update",
            })
        return res
