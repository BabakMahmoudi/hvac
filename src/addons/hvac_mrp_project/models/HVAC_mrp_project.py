from odoo import models, fields, api

class HvacMrpProject(models.Model):
    _name = "hvac.mrp.project"
    _description = 'Manufacturing Project'

    name = fields.Char("Name")
    # company_id = fields.Many2one(
    #     'res.company', 'Company', index=True,
    #     default=lambda self: self.env.company)