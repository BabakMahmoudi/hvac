# -*- coding: utf-8 -*-

from odoo import models, fields, api


class hvac_product_fork(models.Model):
    _inherit = 'product.template'
    is_forkable = fields.Boolean("Is Forkable")



