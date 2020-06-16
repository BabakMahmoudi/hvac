# -*- coding: utf-8 -*-
# from odoo import http


# class HvacProductSpec(http.Controller):
#     @http.route('/hvac_product_spec/hvac_product_spec/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hvac_product_spec/hvac_product_spec/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hvac_product_spec.listing', {
#             'root': '/hvac_product_spec/hvac_product_spec',
#             'objects': http.request.env['hvac_product_spec.hvac_product_spec'].search([]),
#         })

#     @http.route('/hvac_product_spec/hvac_product_spec/objects/<model("hvac_product_spec.hvac_product_spec"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hvac_product_spec.object', {
#             'object': obj
#         })
