from odoo import models, fields, api
from typing import TYPE_CHECKING,Any
if TYPE_CHECKING:
    # from hvac_mrp_project.models.hvac_mrp_project import HvacMrpProject
    # from hvac_mrp_project.models.hvac_utils import HvacUtils
    # from odoo.addons.sale.models.sale import SaleOrder
    # from odoo.addons.sale.models.sale import SaleOrderLine
    # from odoo import models,fields,api
    from hvac_mrp_project.models.hvac_imports import StockMove, StockMoveLine, HvacUtils, HvacMrpProject, \
        HvacSaleOrderLineExtensions, HvacSaleOrderExtensions,HvacMrpProduction, \
        HvacPurchaseOrder, HvacPurchaseOrderLine
        

else:
    HvacMrpProject = models.Model
    HvacUtils = models.Model
    StockMove = models.Model
    StockMoveLine = models.Model
    HvacSaleOrderLineExtensions = models.Model
    HvacSaleOrderExtensions = models.Model
    HvacMrpProduction = models.Model
    HvacPurchaseOrder = models.Model
    HvacPurchaseOrderLine = models.Model

class HvacStockMove(StockMove):
    _inherit = 'stock.move'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HvacStockMove, self).create(vals_list)
        # print('stock move create')
        for val in vals_list:
            sale_order_line_id = val.get("sale_line_id", False)
            if sale_order_line_id:
                print(sale_order_line_id)
        # if self.sale_line_id:
        #     l:HvacSaleOrderLineExtensions = self.sale_line_id
        #     s:HvacSaleOrderExtensions = l.order_id
        #     if s.project_id:
        #         print('Stock Move On Project:{}'.format(s.getProject().name))
        return res
    
    def write(self, vals):
        res = super(HvacStockMove, self).write(vals)
        # print('stock move write')
        return res

    def getCreatedProduction(self)->HvacMrpProduction:
        return self.created_production_id
    
    def getCreatedPurchaseLine(self)->HvacPurchaseOrderLine:
        return self.created_purchase_line_id

class HvacStockMoveLine(StockMoveLine):
    _inherit ="stock.move.line"

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HvacStockMoveLine, self).create(vals_list)
        # print('stock move line create')
        # for l in self:
        #     sale_order_line:HvacSaleOrderLineExtensions = l.sale_line_id
        #     sale_order:HvacSaleOrderExtensions = sale_order_line.order_id
        #     if sale_order.project_id:
        #         print('Stock Move On Project:{}'.format(sale_order.getProject().name))
        # if self.sale_line_id:
        #     l:HvacSaleOrderLineExtensions = self.sale_line_id
        #     s:HvacSaleOrderExtensions = l.order_id
        #     if s.project_id:
        #         print('Stock Move On Project:{}'.format(s.getProject().name))
        return res
    
    def write(self, vals):
        res = super(HvacStockMoveLine, self).write(vals)
        print('stock move line write')
        return res
