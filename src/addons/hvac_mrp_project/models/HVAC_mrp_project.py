from odoo import models, fields, api

class HvacMrpProject(models.Model):
    _name = "hvac.mrp.project"
    _description = 'Manufacturing Project'

    name = fields.Char("Name")
    mf_order = fields.One2many("mrp.production" , "project_id")
    task_ids = fields.One2many('hvac.mrp.tasks' , 'mrp_ref')
    sale_order = fields.Many2one('sale.order')
    # MFO_Name = fields.Many2one('mrp.production')
    # company_id = fields.Many2one(
    #     'res.company', 'Company', index=True,
    #     default=lambda self: self.env.company)

class HvacMrpProduction(models.Model):

    _inherit = 'mrp.production'


    project_id = fields.Many2one('hvac.mrp.project' , "mf_order")
    


class HvacProductionTasks(models.Model):
    _name = "hvac.mrp.tasks"

    name = fields.Char()
    mrp_ref = fields.Many2one("hvac.mrp.project" ,'task_ids' )
    manufacturing_order = fields.Many2one('mrp.production')
    product_id = fields.Many2one('product.product' )







    

    