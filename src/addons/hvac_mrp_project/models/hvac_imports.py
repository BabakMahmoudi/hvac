from typing import TYPE_CHECKING, Any,List, Dict
if TYPE_CHECKING:
    from odoo import models, fields, api
    from odoo.addons.sale.models.sale import SaleOrder
    from odoo.addons.sale.models.sale import SaleOrderLine
    from odoo.addons.product.models.product import ProductProduct
    from odoo.addons.product.models.product_template import ProductTemplate
    from odoo.addons.mrp.models.mrp_bom import MrpBom,MrpBomLine
    from odoo.addons.mrp.models.mrp_production import MrpProduction
    from odoo.addons.stock.models.stock_move import StockMove
    #from odoo.addons.mrp.models.stock_move import StockMove
    from odoo.addons.stock.models.stock_move_line import StockMoveLine
    from odoo.addons.purchase.models.purchase import PurchaseOrder, PurchaseOrderLine
    from hvac_mrp_project.models.hvac_mrp_production_extensions import HvacMrpProduction
    from hvac_mrp_project.models.hvac_mrp_project import HvacMrpProject
    from hvac_mrp_project.models.hvac_utils import HvacUtils
    from hvac_mrp_project.models.hvac_product_extensions import HvacProductExtensions, HvacProductTemplateExtensions
    from hvac_mrp_project.models.hvac_sale_order_extensions import HvacSaleOrderExtensions, HvacSaleOrderLineExtensions
    from hvac_mrp_project.models.hvac_stock_move import HvacStockMove, HvacStockMoveLine
    from hvac_mrp_project.models.hvac_mrp_bom_extensions import HvacMrpBomExtensions, HvacMrpBomLineExtensions
    from hvac_mrp_project.models.hvac_purchase_extensions import HvacPurchaseOrder, HvacPurchaseOrderLine
else:
    HvacMrpProject = models.Model
    HvacUtils = models.Model
    SaleOrder = models.Model
    SaleOrderLine = models.Model
    HvacProductExtensions = models.Model
    HvacProductTemplateExtensions = models.Model
    HvacMrpBomExtensions = models.Model
    HvacMrpBomLineExtensions = models.Model
    ProductProduct = models.Model
    ProductTemplate = models.Model
    MrpBom = models.Model
    MrpBomLine = models.Model
    HvacSaleOrderExtensions = models.Model
    HvacMrpBomLineExtensions = models.Model
    StockMove = models.Model
    StockMoveLine = models.Model
    HvacStockMove = models.Model
    HvacStockMoveLine = models.Model
    MrpProduction = models.Model
    HvacMrpProduction = models.Model
    PurchaseOrder = models.Model
    PurchaseOrderLine = models.Model
    HvacPurchaseOrder = models.Model
    HvacPurchaseOrderLine = models.Model

