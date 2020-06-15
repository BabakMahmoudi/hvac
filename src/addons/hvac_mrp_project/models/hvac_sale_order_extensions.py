
from odoo import models, fields, api
from typing import TYPE_CHECKING,Any
if TYPE_CHECKING:
    # from hvac_mrp_project.models.hvac_mrp_project import HvacMrpProject
    # from hvac_mrp_project.models.hvac_utils import HvacUtils
    # from odoo.addons.sale.models.sale import SaleOrder
    # from odoo.addons.sale.models.sale import SaleOrderLine
    # from odoo import models,fields,api
    from hvac_mrp_project.models.hvac_imports import SaleOrder, SaleOrderLine, HvacMrpProject, HvacUtils

else:
    HvacMrpProject = models.Model
    HvacUtils = models.Model
    SaleOrder = models.Model
    SaleOrderLine = models.Model
    


class HvacSaleOrderExtensions(SaleOrder):
    _inherit = 'sale.order'
    hvac_project_name = fields.Many2one('hvac.mrp.project') 


    
    def creat_task(self):
        aa = self.env['hvac.mrp.project'].search([("sale_order", '=', self.id)]).id
        if aa :
            raise Exception("already exists!")
        else:
            project = self.env['hvac.mrp.project'].create({'name' :self.name})
            project.sale_order = self.id
        orders=self.env['mrp.production'].search([('origin', "=" ,self.name)])


        for line in self.order_line :
            
            task = self.env["hvac.mrp.tasks"].create({'name' : 'task'})
            task.product_id = line.product_id
            task.mrp_ref = project
            
            for order in orders:
                if order.product_id == task.product_id:
                    task.manufacturing_order = order.id
                for bom_line in order.bom_id.bom_line_ids:
                    bom_task = self.env['hvac.mrp.tasks'].create({'name':bom_line.display_name})
                    bom_task.product_id=bom_line.product_id
                    bom_task.mrp_ref = project
            
class HvacSaleOrderLineExtensions(SaleOrderLine):
    _inherit = "sale.order.line"

    """ The bom that will be used for this 
        product when a manufacturing order is
        created from the sale order."""
    bom_id = fields.Many2one("mrp.bom")
    

    def test(self):
        
        """ Hey """
        self.bom_id
        self.test





    

