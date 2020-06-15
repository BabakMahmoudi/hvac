from odoo import models, fields, api
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    # from hvac_mrp_project.models.hvac_mrp_project import HvacMrpProject
    # from hvac_mrp_project.models.hvac_utils import HvacUtils
    # from odoo.addons.mrp.models.mrp_bom import MrpBom
    # from odoo import models,fields,api
    from hvac_mrp_project.models.hvac_imports import\
        HvacProductTemplateExtensions, HvacUtils, HvacMrpProject, MrpBom, MrpBomLine, HvacProductExtensions
else:
    HvacMrpProject = models.Model
    MrpBom = models.Model
    MrpBomLine = models.Model
    HvacProductTemplateExtensions = models.Model
    HvacUtils = models.Model
    HvacProductExtensions = models.Model


class HvacMrpBomExtensions(MrpBom):
    _inherit = 'mrp.bom'

    def getUtils(self) -> HvacUtils:
        return self.env['hvac.utils']

    def fork(self, project: HvacMrpProject, section=False):
        """ Froks a bom for a specific project """
        #utils = self.getUtils()
        #project_attr = utils.getProjectAttributeValue(project.code)
        #product_tmpl: HvacProductTemplateExtensions = self.product_tmpl_id
        result = self.copy()
        # self.flush()
        # self.invalidate_cache()
        for line in result.bom_line_ids:
            l: HvacMrpBomLineExtensions = line
            product_template: HvacProductTemplateExtensions = l.product_tmpl_id
            if (product_template.is_forkable):
                product_template.ensureProject(project, section=section)
                product = product_template.getProjectVariant(
                    project, section=section)
                l.product_id = product
                product_template.fork(project, l.child_bom_id, section=section)
            else:
                # product is not forkable
                pass
        return result


class HvacMrpBomLineExtensions(MrpBomLine):
    _inherit = 'mrp.bom.line'
