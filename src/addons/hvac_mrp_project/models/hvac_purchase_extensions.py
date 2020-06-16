from odoo import models, fields, api
from typing import TYPE_CHECKING,Any
if TYPE_CHECKING:
    # from hvac_mrp_project.models.hvac_mrp_project import HvacMrpProject
    # from hvac_mrp_project.models.hvac_utils import HvacUtils
    # from odoo.addons.sale.models.sale import SaleOrder
    # from odoo.addons.sale.models.sale import SaleOrderLine
    # from odoo import models,fields,api
    from hvac_mrp_project.models.hvac_imports import PurchaseOrder, PurchaseOrderLine
        

else:
    PurchaseOrder = models.Model
    PurchaseOrderLine = models.Model

class HvacPurchaseOrder(PurchaseOrder):
    _inherit = "purchase.order"

class HvacPurchaseOrderLine(PurchaseOrderLine):
    _inherit = 'purchase.order.line'