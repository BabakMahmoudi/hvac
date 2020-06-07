from odoo import models, fields, api


class hvac_fork_wizard(models.TransientModel):
    _name = "hvac.fork.wizrad"
    _description = "Recommended products for current sale order"
    fork_label = fields.Char()
    product_id = fields.Many2one(
        "product.template",
        "Product",
        default=lambda self: self._default_product_id(),
        required=True,
        readonly=True,
        ondelete="cascade",
    )

    def action_fork(self):
        a = self.product_id
        self.fork_product(a, self.fork_label)
        print(a)

    def fork_product(self, product, label):
        if product.is_forkable:
            forked = False
            # if product.is_product_variant:
            #     forked = product.product_tmpl_id.copy()
            # else:
            #     forked = product.copy()
            forked = product.copy()
            forked.name = product.name + label
            name = forked.name
            print(name)
            bom = self.find_bom(product)
            if bom:
                forked_bom = bom.copy()
                if forked.is_product_variant:
                    forked_bom.product_id = forked
                    #forked_bom.product_tmpl_id = forked
                else:
                    forked_bom.product_tmpl_id = forked
                #forked_bom.product_tmpl_id = forked.id
                for bom_line in forked_bom.bom_line_ids:
                    if bom_line.product_id:
                        forked_line_product = self.fork_product(
                             bom_line.product_id, label)
                        print(forked_line_product)
                        bom_line.product_id = False
                        if forked_line_product.is_product_variant:
                            bom_line.product_id = forked_line_product.id
                            bom_line.product_tmpl_id = forked_line_product.product_tmpl_id.id
                        else:
                            bom_line.product_tmpl_id = forked_line_product
                            bom_line.product_id = forked_line_product.product_variant_id.id
            return forked
        return product

    def find_bom(self, product):
        if product:
            for bom in product.bom_ids:
                return bom
        return False

    @api.model
    def _default_product_id(self):
        return self.env.context.get("active_id", False)
