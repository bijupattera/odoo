# -*- coding: utf-8 -*-
from odoo import models, fields, api
class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'
    name = fields.Char('Title', required=True)
    short_name = fields.Char(
        string='Short Title',
        size=100,  # For Char only
        translate=False,  # also for Text fields
    )
    notes = fields.Text('Internal Notes')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')],
        'State')
    description = fields.Html(
        string='Description',
        # optional:
        sanitize=True,
        strip_style=False,
        translate=False,
    )
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner', string='Authors')
    date_updated = fields.Datetime('Last Updated')
    reader_rating = fields.Float(
        'Reader Average Rating',
        (14, 4),  # Optional precision (total, decimals),
    )

    pages = fields.Integer(
        string='Number of Pages',
        default=0,
        help='Total book page count',
        groups='base.group_user',
        # states={'cancel': [('readonly', True)]},
        copy=True,
        index=False,
        readonly=False,
        required=False,
        company_dependent=False,
    )

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))]
        )
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)
        default['name'] = new_name
        return super(LibraryBook, self).copy(default)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book title must be unique.')
    ]

    @api.constrains('date_release')
    def _check_release_date(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise models.ValidationError("Release date must be in the past")

