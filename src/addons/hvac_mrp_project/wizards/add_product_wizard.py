from odoo import models, fields, api


class AddProductWizard(models.TransientModel):
    _name = "hvac.mrp.project.add.product.wizard"

    name = fields.Char(String="Name")
    # section = fields.Selection([
    #     ('1', '1'), ('2', '2'), 
    #     ('3', '3'), ('4', '4'), 
    #     ('5', '5'), ('3', '3')])
    product_tmpl_id = fields.Many2one(
        "product.template",
        "Product",
        required=True,
    )
    product_id = fields.Many2one(
        'product.product', 'Product Variant',
        check_company=True,
        domain="[('product_tmpl_id', '=', product_tmpl_id), ]",
        help="If a product variant is defined the BOM is available only for this product."
    )
    bom_id = fields.Many2one(
        "mrp.bom",
        "Bill of Material",
        required=False,
        readonly=False,
        domain="[('product_tmpl_id', '=', product_tmpl_id), ]"
    )

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

    def action_addProduct(self):

        if self.project_id:
            project = self.project_id
            sale_oder = project.getSaleOrder(True)
            product = project.addProduct(self.product_tmpl_id, self.bom_id)
        else:
            print('No project id')

        print('action do')
