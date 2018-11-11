# -*- coding: utf-8 -*-
from odoo import http

# class LibraryBooks(http.Controller):
#     @http.route('/library_books/library_books/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/library_books/library_books/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('library_books.listing', {
#             'root': '/library_books/library_books',
#             'objects': http.request.env['library_books.library_books'].search([]),
#         })

#     @http.route('/library_books/library_books/objects/<model("library_books.library_books"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('library_books.object', {
#             'object': obj
#         })