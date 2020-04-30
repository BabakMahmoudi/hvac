# -*- coding: utf-8 -*-
# from odoo import http


# class Hvac-project(http.Controller):
#     @http.route('/hvac-project/hvac-project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hvac-project/hvac-project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hvac-project.listing', {
#             'root': '/hvac-project/hvac-project',
#             'objects': http.request.env['hvac-project.hvac-project'].search([]),
#         })

#     @http.route('/hvac-project/hvac-project/objects/<model("hvac-project.hvac-project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hvac-project.object', {
#             'object': obj
#         })
