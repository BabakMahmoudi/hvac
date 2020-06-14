from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from hvac_mrp_project.models.hvac_mrp_project import HvacMrpProject
    from hvac_mrp_project.models.hvac_utils import HvacUtils
    from hvac_mrp_project.models.hvac_product_extensions import HvacProductExtensions, HvacProductTemplateExtensions
    from odoo.addons.sale.models.sale import SaleOrder
    from odoo.addons.sale.models.sale import SaleOrderLine
    from odoo.addons.product.models.product import ProductProduct
    from odoo.addons.product.models.product_template import ProductTemplate
    from odoo.addons.mrp.models.mrp_bom import MrpBom,MrpBomLine

    from hvac_mrp_project.models.hvac_mrp_bom_extensions import HvacMrpBomExtensions, HvacMrpBomLineExtensions
    from odoo import models, fields, api
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
