from odoo import models, fields, api
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from hvac_mrp_project.models.hvac_imports import \
        ProductTemplate, ProductProduct, HvacMrpProject, HvacUtils, models, api
    # from hvac_mrp_project.models.hvac_mrp_project import HvacMrpProject
    # from hvac_mrp_project.models.hvac_utils import HvacUtils
    # from odoo.addons.product.models.product import ProductProduct
    # from odoo.addons.product.models.product_template import ProductTemplate
    # from odoo.addons.sale.models.sale import SaleOrderLine
    # from odoo import models,fields,api
else:
    HvacMrpProject = models.MissingError
    HvacUtils = models.Model
    ProductTemplate = models.Model
    ProductProduct = models.Model


class HvacProductExtensions(ProductProduct):
    _inherit = 'product.product'
    #_name ='hvac.product.extensions'

    def getUtils(self) -> HvacUtils:
        return self.env['hvac.utils']

    def fork(self, project: HvacMrpProject):
        """
            Forks a product as a project variant.
        """
        print("fork")


class HvacProductTemplateExtensions(ProductTemplate):
    _inherit = 'product.template'
    #_name ='hvac.product.template.extensions'
    is_forkable = fields.Boolean("Is Forkable")

    def getUtils(self) -> HvacUtils:
        return self.env['hvac.utils']
    def getProjectVariant(self, project: HvacMrpProject, auto_create=True)->HvacProductExtensions:
        """ 
            Gets or creates a project variant for this template
        """
        utils = self.getUtils()
        utils.ensureProjectAttributeIsSelectedOnProductTemplate(
            self, project.code)
        result = utils.createProjectProductVariant(self, project.code)

        return result

    def ensureProjectVariant(self):
        utils = self.getUtils()
        try:
            # for record in self:
            utils.ensureProjectAttributeLineOnProjectTemplate(self)
        except:
            print("An error occured")

    @api.onchange('is_forkable')
    def is_forkable_changed(self):
        if self.is_forkable:
            self.ensureProjectVariant()
        # for record in self:
        #     if record.is_forkable:
        #         self.ensureProjectVariant()
