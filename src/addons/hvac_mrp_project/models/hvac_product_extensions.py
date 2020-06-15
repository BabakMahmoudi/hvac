from odoo import models, fields, api
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from hvac_mrp_project.models.hvac_imports import \
        HvacMrpBomExtensions, HvacMrpBomLineExtensions, ProductTemplate, ProductProduct, \
        HvacMrpProject, HvacUtils, models, api
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
    HvacMrpBomExtensions = models.Model
    HvacMrpBomLineExtensions = models.Model


class HvacProductExtensions(ProductProduct):
    _inherit = 'product.product'
    #_name ='hvac.product.extensions'

    def getUtils(self) -> HvacUtils:
        return self.env['hvac.utils']

    def fork(self, project: HvacMrpProject, bom: HvacMrpBomExtensions = False, section=False):
        """
            Forks a product as a project variant.
        """
        print("fork")
        if not self.product_tmpl_id.is_forkable:
            return self
        if self.is_already_forked():
            return self
        if not bom:
            bom: HvacMrpBomExtensions = self.get_best_bom_for_forking(project)
        if bom:
            bom: HvacMrpBomLineExtensions = bom.fork(project, section=section)
            bom.bom_product_template_attribute_value_ids = False
            bom.product_id = self
            bom.code = '{}'.format(self.get_project_code())
        return self

    def get_project_code(self):
        result = ''
        try:
            result = self.product_template_attribute_value_ids[0].product_attribute_value_id.name
        except:
            pass
        return result

    def is_already_forked(self):
        """
            Returns true if this product has already been
            forked in this project.
        """
        boms = self.get_boms()
        return boms and len(self.get_boms()) > 0

    def get_best_bom_for_forking(self, project: HvacMrpProject) -> HvacMrpBomLineExtensions:
        tmpl: HvacProductTemplateExtensions = self.product_tmpl_id
        return tmpl.get_best_bom(project)

    def get_boms(self) -> HvacMrpBomExtensions:
        result = self.bom_ids.filtered(lambda x:
                                       x.product_id == self)

        return result


class HvacProductTemplateExtensions(ProductTemplate):
    _inherit = 'product.template'
    
    is_forkable = fields.Boolean("Is Forkable")

    def getUtils(self) -> HvacUtils:
        return self.env['hvac.utils']

    def ensureProject(self, project: HvacMrpProject, section=False):
        """
            Ensures that variants are correctly configured for
            this product template (i.e. the template allows variants for this 
            section of this project).
            Actually it configures the 'Project' attribute on this template
            to include the 'Project_Section' combination code for this product.
        """
        utils = self.getUtils()
        code = utils.getProjectSectionCode(project.code, section)
        utils.ensureProjectAttributeIsSelectedOnProductTemplate(
            self, code)
        return self

    def getProjectVariant(self, project: HvacMrpProject, section=False, auto_create=True) -> HvacProductExtensions:
        """ 
            Gets or creates a variant of this template for 
            a section of the project. Note that a single product
            will have different variants in different sections of
            a project.
        """
        utils = self.getUtils()
        code = utils.getProjectSectionCode(project.code, section)
        utils.ensureProjectAttributeIsSelectedOnProductTemplate(
            self, code)
        value = utils.getProjectAttributeValue(code)
        result = self.product_variant_ids.filtered(lambda x:
                x.product_template_attribute_value_ids.product_attribute_value_id .__contains__(value))
        # already_exists = \
        #     self.product_variant_ids and \
        #     self.product_variant_ids. \
        #         product_template_attribute_value_ids.product_attribute_value_id.__contains__(value)
        # self.product_variant_ids.product_template_attribute_value_ids
        # for product in self.product_variant_ids:
        #     p:HvacProductExtensions = product
        #     p.product_template_attribute_value_ids
        if not result and auto_create:
            result = utils.createProjectProductVariant(self, code)
        return result

    # def get_project_variant(self, project_code: str) -> HvacProductExtensions:
    #     utils = self.getUtils()
    #     value = utils.getProjectAttributeValue(project_code)
    #     return self.product_variant_ids.filtered(lambda x: x.product_template_attribute_value_ids.product_attribute_value_id .__contains__(value))

    def fork(self, project: HvacMrpProject, bom: HvacMrpBomExtensions = False, section=False) -> HvacProductExtensions:
        """
            Forks a product template by creating the project variant
            and forking the bom.
            Note that a single product can be forked differently in
            different sections of a project.
        """
        result = self.product_variant_id
        #result = self.get_best_bom(project)
        if self.is_forkable:
            result = self.getProjectVariant(
                project, section=section, auto_create=True)
            result.fork(project, False, section=section)

        return result

    def get_best_bom(self, project: HvacMrpProject) -> HvacMrpBomExtensions:
        """
            Gets the best bom for forking this product template in 
            the specified project.
        """
        #return self.bom_ids
        if len(self.bom_ids.ids) > 0:
            return self.bom_ids[0]
        return False
    # def ensureProjectVariant(self):
    #     utils = self.getUtils()
    #     try:
    #         # for record in self:
    #         utils.ensureProjectAttributeLineOnProjectTemplate(self)
    #     except:
    #         print("An error occured")

    # @api.onchange('is_forkable')
    # def is_forkable_changed(self):
    #     if self.is_forkable:
    #         self.ensureProjectVariant()
    #     # for record in self:
    #     #     if record.is_forkable:
    #     #         self.ensureProjectVariant()
