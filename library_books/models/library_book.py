# -*- coding: utf-8 -*-
from oodoo import models, fields
class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'
    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title')
    notes = fields.Text('Internal Notes')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')],
        'State')
    description = fields.Html('Description')
    cover = fields.Binary('Book Cover')
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner', string='Authors')

    def name_get(self):
        result = []
            for record in self:
            result.append(
            (record.id,
                u"%s (%s)" % (record.name, record.date_released)
    ))
    return result