from odoo import models, fields, api
from typing import TYPE_CHECKING, Any,List

if TYPE_CHECKING:
    from hvac_mrp_project.models.hvac_imports import \
        HvacProductExtensions, HvacProductTemplateExtensions, HvacUtils, \
        HvacMrpBomExtensions, HvacMrpBomLineExtensions, HvacSaleOrderLineExtensions, \
        HvacSaleOrderExtensions, HvacStockMove, HvacStockMoveLine,HvacMrpProduction, \
        HvacPurchaseOrderLine, HvacPurchaseOrder,RecalculateProjectWizard
else:
    HvacBom = Any
    HvacMrpBomExtensions = models.Model
    MrpBom = False
    HvacProductTemplateExtensions = models.Model
    HvacUtils = models.Model
    HvacMrpBomLineExtensions = models.Model
    HvacMrpBomLineExtensions = models.Model
    HvacUtils = models.Model
    HvacProductExtensions = models.Model
    HvacSaleOrderLineExtensions = models.Model
    HvacSaleOrderExtensions = models.Model
    HvacStockMove = models.Model
    HvacStockMoveLine = models.Model
    HvacMrpProduction = models.Model
    HvacPurchaseOrderLine = models.Model
    HvacPurchaseOrder = models.Model
    RecalculateProjectWizard = models.Model

class HvacMrpTask(models.Model):
    _name = 'hvac.mrp.task'
    name = fields.Char()
    project_id = fields.Many2one("hvac.mrp.project")
    sequence = fields.Integer(string='Sequence', default=10)
    TYPE_MO = 'MO'
    TYPE_PO = 'PO'
    TYPE_EN = 'EN'
    TYPE_LO = 'LO'
    TYPE_OT = 'OT'
    task_type = fields.Selection(
        [(TYPE_MO, 'Manufacturing'), (TYPE_PO, 'Purchase'), (TYPE_EN, 'Engineering'), 
        (TYPE_LO, 'Logistic'), (TYPE_OT, 'Other')],
        default='',
        String="Type")

    manufacturing_order = fields.Many2one('mrp.production')
    product_id = fields.Many2one('product.product')
    purchase = fields.Many2one("purchase.order.line")
    planned_start = fields.Date()
    planned_finish = fields.Date()
    responsible_id = fields.Many2one(
        'res.users', string='Responsible', default=lambda self: self.env.uid, company_dependent=True, check_company=True,
        help="This user will be responsible of the next activities related to logistic operations for this product.")
    parent_task = fields.Many2one('hvac.mrp.task')

    def get_manufacturing_order(self)->HvacMrpProduction:
        return self.manufacturing_order
    def get_task_for_purchase(self , PO:HvacPurchaseOrderLine , project):
        result = self.env[self._name].search([
            ('purchase', '=', PO.id),('project_id','=',project.id)])
        if not result :
            result = self.env[self._name].create({
            'purchase': PO.id ,
            'project_id' : project.id,
            'name' : PO.name
            
            }) 
        return result 
        
    def get_task_for_production(self , MO:HvacMrpProduction , project):
        result = self.env[self._name].search([
            ('manufacturing_order', '=', MO.id),('project_id','=',project.id)])
        if not result :
            result = self.env[self._name].create({
            'manufacturing_order': MO.id ,
            'project_id' : project.id,
            'planned_start' : MO.date_planned_start,
            'planned_finish' : MO.date_planned_finished,
            'name' : 'manufacture : {}'.format(MO.name)
            }) 
        return result 

    def get_default_name(self):
        res =  ''
        if self.manufacturing_order:
            res = 'Manufacture {}'.format(self.get_manufacturing_order().product_tmpl_id.name)
        if self.purchase:
            res = 'Purchase {}'.format(self.purchase.name)
        return res        
    
    def get_default_task_type(self):
        if self.manufacturing_order:
            return self.TYPE_MO
        if self.purchase:
            return self.TYPE_PO
        return self.TYPE_OT
        
            

    def recalculate(self,options:RecalculateProjectWizard):
        
        self.task_type = self.get_default_task_type()
        self.name = self.get_default_name()
        self.parent_task = self


        return self


        




# class HvacMrpProjectProductLine(models.Model):
#     _name = "hvac.mrp.project.product.line"
#     project_id = fields.Many2one("hvac.mrp.project")

#     product
