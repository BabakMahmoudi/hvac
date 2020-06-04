# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sandbox(models.Model):
    _name = 'sandbox.sandbox'
    _description = 'sandbox.sandbox'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
    def generate_record_name(self):
        print("hi there")
        
