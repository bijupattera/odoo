# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Course(models.Model):
    _name = 'oa.course'
    _description = 'Open Academy Course Class'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many('oa.session', 'course_id', string="Sessions")

class Session(models.Model):
    _name = 'oa.session'
    _description = 'Open Academy Sesions'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(5, 2), help="Number of days")
    seats = fields.Integer(string="Seats")
    instructor_id = fields.Many2one('res.partner', string="Instructor")
    course_id = fields.Many2one('oa.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
