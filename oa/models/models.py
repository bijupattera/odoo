# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Course(models.Model):
    _name = 'oa.course'
    _description = 'OPen Academy Course Class'
    name = fields.Char(string="Title", required=True)
    description = fields.Text()