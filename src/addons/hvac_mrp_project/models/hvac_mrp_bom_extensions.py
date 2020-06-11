from odoo import models, fields, api
from typing import TYPE_CHECKING,Any
if TYPE_CHECKING:
    from hvac_mrp_project.models.hvac_mrp_project import HvacMrpProject
    from hvac_mrp_project.models.hvac_utils import HvacUtils
    from odoo.addons.mrp.models.mrp_bom import MrpBom
    from odoo import models,fields,api
else:
    HvacMrpProject = Any
    HvacUtils = Any
    MrpBom = models.Model

class HvacMrpBomExtensions(MrpBom):
    _inherit = 'mrp.bom'
    def getUtils(self) -> HvacUtils:
        return self.env['hvac.utils']

    def fork(self, project: HvacMrpProject):
        """ Froks a bom for a specific project """
        utils = self.getUtils()
        project = utils.getProjectAttributeValue(project.code)
        
        
        



        print('fork')


class HvacMrpBomLineExtensions(models.Model):
    _inherit = 'mrp.bom.line'
