# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Course(models.Model):
    _name = 'oa.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()