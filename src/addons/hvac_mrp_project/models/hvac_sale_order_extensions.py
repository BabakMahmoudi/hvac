
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
    project_id = fields.Many2one('hvac.mrp.project',string="Manufacturing Project") 


<<<<<<< HEAD
<<<<<<< HEAD:src/addons/hvac_mrp_project/models/sale_order_mrp_project.py
    def ImportBom(self , bom_id , project):

        for bom_line in bom_id.bom_line_ids:
            bom_task = self.env['hvac.mrp.tasks'].create({'name':bom_line.display_name})
            bom_task.product_id=bom_line.product_id
            bom_task.mrp_ref = project 
            self.ImportBom(bom_line.child_bom_id , project)


=======
>>>>>>> ed63681ab88c6936f1fb86fbbea5c3121556b072:src/addons/hvac_mrp_project/models/hvac_sale_order_extensions.py
=======
    def getProject(self)->HvacMrpProject:
        return self.project_id
>>>>>>> dd35533885003db51b24d955f944be5884d3cafd
    
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
<<<<<<< HEAD
                    self.ImportBom(order.bom_id , project)
            
=======
                for bom_line in order.bom_id.bom_line_ids:
                    bom_task = self.env['hvac.mrp.tasks'].create({'name':bom_line.display_name})
                    bom_task.product_id=bom_line.product_id
                    bom_task.mrp_ref = project
    
    # @api.onchange('state')
    # def on_state_change(self):
    #     print('state changed ' + self.state)



    # we failed to apply  @api.onchange('state')
    # therefore we stick to overriding the write method
    def write(self, values):
        res = super(HvacSaleOrderExtensions, self).write(values)
        if values.get('state',False):
            self.onSaleOrderStateChanged(values.get('state',False))
        # print ('write')
        return res

    # def _action_confirm(self):
    #     print('confirmed ' + self.state)
    #     res = super()._action_confirm()
    #     self.onSaleOrderStateChanged()
    #     return res

    def onSaleOrderStateChanged(self, val):
        print('Sale Order State Changed: {}'.format(val))
        p:HvacMrpProject = self.project_id
        if p:
            p.onSaleOrderStatusChanged(self,val)
        pass

    
>>>>>>> dd35533885003db51b24d955f944be5884d3cafd
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





    

