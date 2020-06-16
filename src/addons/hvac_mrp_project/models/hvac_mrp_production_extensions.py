from odoo import models, fields, api

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from hvac_mrp_project.models.hvac_imports import \
        MrpProduction, HvacStockMove
else:
    MrpProduction = models.Model
    HvacStockMove = models.Model


class HvacMrpProduction(MrpProduction):

    _inherit = 'mrp.production'
    project_id = fields.Many2one('hvac.mrp.project', "mf_order")

    def getRawComponentsMove(self) -> HvacStockMove:
        return self.move_raw_ids
