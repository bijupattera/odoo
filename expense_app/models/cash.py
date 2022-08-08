from odoo import api, fields, models


class cashinhand(models.Model):
    _name = 'cash.inhand'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Cash in Hand AC'
    _order = 'date desc'

    name = fields.Char(
        'Purticulers',
        default=None,
        index=True,
        help='Debit What Comes In and Credit What Goes Out',
        readonly=False,
        tracking=True,
        required=True,
        translate=False,
    )

    notes = fields.Text('Notes')
    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True
    )
    date = fields.Datetime(
        'Dated On',
        default=lambda self: fields.Datetime.now())
    # default=lambda self: fields.Date.today().replace(month=1)) for month of Jan
    debit = fields.Float('Debit', tracking=True)
    credit = fields.Float('Credit', tracking=True)
    balance = fields.Float('Balance', compute="_compute_balance")


    @api.depends("debit", "credit")
    def _compute_balance(self):
        for r in self:
            sum_debit = sum(self.env["cash.inhand"].search([('create_date', '<=', r.create_date)]).mapped('debit'))
            sum_credit = sum(self.env["cash.inhand"].search([('create_date', '<=', r.create_date)]).mapped('credit'))
            r.balance = sum_debit - sum_credit

    def write(self, vals):
        res = super(cashinhand, self).write(vals)
        sum_debit = sum(self.env["cash.inhand"].search([]).mapped('debit'))
        sum_credit = sum(self.env["cash.inhand"].search([]).mapped('credit'))
        vals['balance'] = sum_debit - sum_credit
        # update Cash in Hand
        wt = self.env['fd.invest']
        cashid = wt.search([('name', '=', 'Cash in Hand')]).id
        wt.browse(cashid).write({
            'create_uid': self.env.user.id,
            'date': fields.Date.today(),
            'value': vals['balance'],
            'invested': vals['balance'],
            'notes': "Auto Updated By Model CashInHand Write",
        })
        return res

    @api.model
    def create(self, vals):
        res = super(cashinhand, self).create(vals)
        sum_debit = sum(self.env["cash.inhand"].search([]).mapped('debit'))
        sum_credit = sum(self.env["cash.inhand"].search([]).mapped('credit'))
        vals['balance'] = sum_debit - sum_credit
        # update Cash in Hand
        wt = self.env['fd.invest']
        cashid = wt.search([('name', '=', 'Cash in Hand')]).id
        wt.browse(cashid).write({
            'create_uid': self.env.user.id,
            'date': fields.Date.today(),
            'value': vals['balance'],
            'invested': vals['balance'],
            'notes': "Auto Updated By Model Cashinhand Create",
        })
        return res


    def unlink(self):
        res = super().unlink()
        sum_debit = sum(self.env["cash.inhand"].search([]).mapped('debit'))
        sum_credit = sum(self.env["cash.inhand"].search([]).mapped('credit'))
        balance = sum_debit - sum_credit
        # update Cash in Hand
        wt = self.env['fd.invest']
        cashid = wt.search([('name', '=', 'Cash in Hand')]).id
        wt.browse(cashid).write({
            'create_uid': self.env.user.id,
            'date': fields.Date.today(),
            'value': balance,
            'invested': balance,
            'notes': "Auto Updated By Model Cashinhand Unlink on : " + str(fields.Datetime.now()),
        })
        return res
