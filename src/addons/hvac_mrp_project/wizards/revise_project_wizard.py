from odoo import models, fields, api
from datetime import datetime


class ReviseProjectWizard(models.TransientModel):
    _name = "hvac.mrp.project.revise.project.wizard"

    reschedule= fields.Boolean(string="Reschedule",
        default= False,
        help="help")
    revise_sale_order = fields.Boolean(
        string="Revise Sale Odrder",
        default= False,
        help="If set the current sale will be canceled and a new sale order is created.")
    revise_bom = fields.Boolean(
        string="Revise BoM",
        default= False,
        help="If set the current sale will be canceled and a new sale order is created."
        )
    replan= fields.Boolean(string="Replan",
        default= False,
        help="help")
    update_progress = fields.Boolean(
        
    )

    status_date = fields.Date(
        string='Status Date',
        default = datetime.today())
    
    reason = fields.Char()
    



    project_id = fields.Many2one(
        "hvac.mrp.project",
        "Project",
        default=lambda self: self._default_project_id(),
        required=True,
        readonly=True,
        ondelete="cascade",
    )

    @api.model
    def _default_project_id(self):

        return self.env.context.get("active_id", False)


    def action_revise(self):
        if self.project_id:
            project = self.project_id
            project.revise(self)
        print('revise')


