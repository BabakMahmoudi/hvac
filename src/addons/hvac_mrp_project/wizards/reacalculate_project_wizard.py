from odoo import models, fields, api


class RecalculateProjectWizard(models.TransientModel):
    _name = "hvac.mrp.project.recalculate.project.wizard"

    reschedule= fields.Boolean(string="Reschedule",help="help")
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


    def action_recalculate(self):
        if self.project_id:
            project = self.project_id
            project.Recalculate(self)
        print('recalculate')


