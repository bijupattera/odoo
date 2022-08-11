from datetime import date
from dateutil import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

class fd(models.Model):
    _name = 'fd.invest'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Investment Tracker'
    _order = 'date desc'

    name = fields.Char(
        'Deposit',
        default=None,
        index=True,
        help='Deposit Scheme name',
        readonly=False,
        required=True,
        translate=False,
        tracking=True,
    )
    category = fields.Selection(
        [('sip', 'SIP'),
         ('insurance', 'Insurance'),
         ('fd', 'Fixed Deposite'),
         ('property', 'Property'),
         ('cash', 'Cash'),
         ('deptors', 'Deptors'),
         ('sd', 'Savings Deposite')],
        default='fd',
        tracking=True,
    )
    notes = fields.Text('Notes')
    descr = fields.Text('Description')
    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True
    )

    invested = fields.Float('Invested ₹', tracking=True,)
    gain = fields.Float('Gain ₹', compute="_compute_gain")
    quantity = fields.Float('#Deposits', default=1, tracking=True,)
    value = fields.Float('Present Value ₹', tracking=True,)
    total = fields.Float('Total ₹', compute="_compute_total")
    maturity = fields.Date('Maturity Date', default=fields.Date.today())
    info_due_date = fields.Boolean('Maturity Info Due', compute="_info_due_date")

    @api.depends("maturity")
    def _info_due_date(self):
        for rec in self:
            today = date.today()
            # how many days before the Maturity date alerts to show, fetching from ir.config.parameter table
            days = self.env['ir.config_parameter'].get_param('expense_app.maturity_due_warning')
            due_start = rec.maturity - relativedelta.relativedelta(days=int(days))
            if due_start < date.today():
                rec.info_due_date = True
            else:
                rec.info_due_date = False

    def action_info_due_date(self):
        for record in self:
            today = date.today()
            secret = self.env['ir.config_parameter'].get_param('expense_app.maturity_due_warning')
            due_date = record.maturity - relativedelta.relativedelta(days=int(secret))
            if due_date < date.today():
                record.info_due_date = True
            else:
                record.info_due_date = False
            print(record.name, due_date)

    @api.depends("invested")
    def _compute_total(self):
        for record in self:
            record.total = record.invested * record.quantity
            
    @api.depends("value", "invested")
    def _compute_gain(self):
        for record in self:
            record.gain = record.value - record.total
            if record.gain > 0:
                record.stage_id = 'gain'
            elif record.gain < 0:
                record.stage_id = 'loss'
            else:
                record.stage_id = 'new'
            
    date = fields.Date(
        'Dated On',
        default=lambda self: fields.Date.today())
        # default=lambda self: fields.Date.today().replace(month=1)) for month of Jan
    date_clossed = fields.Date('Clossed On', readonly=True)
    active = fields.Boolean('Active?', default=True)
    bank = fields.Many2many('res.partner', string='Bank')
    years = fields.Integer(default=1)
    color = fields.Integer('Color Index')

    @api.depends("gain")
    def _compute_kstate(self):
        for record in self:
            if record.gain > 1:
                record.kanban_state = 1
            elif record.gain < 0:
                record.kanban_state = 2
            else:
                record.kanban_state = 0
          
    kanban_state = fields.Char('Kanban State', compute="_compute_kstate")
    priority = fields.Selection(
        [('0', 'Low'),
         ('1', 'Normal'),
         ('2', 'Medium'),
         ('3', 'High')],
        'Priority',
        default='1')
    
    state = fields.Selection(
        [('open','Open'),
         ('clossed','Clossed')],
        default='open',
    )
    
    def make_inactive(self):
        self.ensure_one()
        self.active = False    
    
    def button_close(self):
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_('FD or SIP is not in a state for clossing'))
        self.stage_id = self.state = 'clossed'
        self.date_clossed = fields.Date.today()
        self.env['cash.inhand'].create({
            'name': self.name,
            'create_uid': self.env.user.id,
            'debit': self.value,
            'date': fields.Date.today()
        })
        # self.make_inactive() gives a read permission error but all updates are sucess ????
    
    stage_id = fields.Selection(
        [('new','No Gain/Loss'),
         ('gain','Gain'),
         ('loss','Loss'),
         ('clossed','Clossed')],
        default='new',
    )
