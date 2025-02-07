# -*- coding: utf-8 -*-
# from odoo import http


# class Ordezkaritzak(http.Controller):
#     @http.route('/ordezkaritzak/ordezkaritzak', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ordezkaritzak/ordezkaritzak/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ordezkaritzak.listing', {
#             'root': '/ordezkaritzak/ordezkaritzak',
#             'objects': http.request.env['ordezkaritzak.ordezkaritzak'].search([]),
#         })

#     @http.route('/ordezkaritzak/ordezkaritzak/objects/<model("ordezkaritzak.ordezkaritzak"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ordezkaritzak.object', {
#             'object': obj
#         })

