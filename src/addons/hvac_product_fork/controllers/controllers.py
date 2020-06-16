# -*- coding: utf-8 -*-
# from odoo import http


# class HvacProject(http.Controller):
#     @http.route('/hvac_project/hvac_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hvac_project/hvac_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hvac_project.listing', {
#             'root': '/hvac_project/hvac_project',
#             'objects': http.request.env['hvac_project.hvac_project'].search([]),
#         })

#     @http.route('/hvac_project/hvac_project/objects/<model("hvac_project.hvac_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hvac_project.object', {
#             'object': obj
#         })
