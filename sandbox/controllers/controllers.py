# -*- coding: utf-8 -*-
from odoo import http


class Sandbox(http.Controller):
    @http.route('/sandbox/sandbox/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/sandbox/sandbox/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('sandbox.listing', {
            'root': '/sandbox/sandbox',
            'objects': http.request.env['sandbox.sandbox'].search([]),
        })

    @http.route('/sandbox/sandbox/objects/<model("sandbox.sandbox"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('sandbox.object', {
            'object': obj
        })
