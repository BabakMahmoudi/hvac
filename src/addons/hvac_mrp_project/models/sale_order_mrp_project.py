
from odoo import models, fields, api

class HvacSaleOrderExtensions(models.Model):
    _inherit = 'sale.order'
 

    hvac_project_name = fields.Many2one('hvac.mrp.project') 

    

