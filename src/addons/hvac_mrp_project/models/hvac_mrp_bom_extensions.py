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
    state = fields.Selection([
        ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'),('retired','Retired')],
        default='draft',
        string='Status',
        copy = True
    )
    revision = fields.Integer(string='Revision', default=0,copy=True)

    def getUtils(self) -> HvacUtils:
        return self.env['hvac.utils']

    def revise(self,forced=False):
        res = self
        if self.state !='draft' or forced:
            res:HvacMrpBomExtensions = self.copy()
            self.write({
                'state': 'retired',
                'active':False
                })
            res.revision = res.revision + 1
            res.state = 'draft'
            res.code = 'Rev ({})'.format(res.revision)
            for _line in self.bom_line_ids:
                line:HvacMrpBomLineExtensions = _line
                bom:HvacMrpBomExtensions =  line.child_bom_id
                if bom:
                    bom.revise(forced=True)
                

        return res

    def fork(self, project: HvacMrpProject, section=False):
        """ Froks a bom for a specific project """
        result = self.copy()
        result.revision = 0
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
