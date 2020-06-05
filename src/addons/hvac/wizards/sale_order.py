from odoo import models, fields, api

class hvac__wizard_sale(models.TransientModel):
    __name = 'hvac__wizard_sale'

    main_product = fields.Many2one('product.template')
    new_product = fields.Char()
    main_BOM = fields.Many2one('mrp.bom')
    new_BOM = fields.Char()

    def create_product(self):


        # product = self.env['product.template'].create({'name' :self.main_product.name})
        product = self.main_product.copy()
        product.name = self.new_product
        BOM = self.main_BOM.copy()
        BOM.product_tmpl_id = product.id
      
        