from odoo import models, fields, api
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from hvac_mrp_project.models.hvac_imports import \
    HvacProductExtensions, HvacProductTemplateExtensions, HvacUtils, HvacMrpBomExtensions, HvacMrpBomLineExtensions
else:
    HvacBom = Any
    HvacMrpBomExtensions = models.Model
    MrpBom = False
    HvacProductTemplateExtensions = models.Model
    HvacUtils = models.Model
    HvacMrpBomLineExtensions = models.Model
    HvacMrpBomLineExtensions = models.Model
    HvacUtils = models.Model
    HvacProductExtensions = models.Model


class HvacMrpProject(models.Model):
    _name = "hvac.mrp.project"
    _description = 'Manufacturing Project'

    name = fields.Char("Name")
    code = fields.Char(string='Code', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: self._default_code())

    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=False,
        #states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        #domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    sale_order_lines = fields.One2many(
        'sale.order.line', compute='_compute_sale_order_lines', readonly=True)

    mf_order = fields.One2many("mrp.production", "project_id")
    task_ids = fields.One2many('hvac.mrp.tasks', 'mrp_ref')
    sale_order_id = fields.Many2one('sale.order')

    def getUtils(self) -> HvacUtils:
        return self.env['hvac.utils']

    """
        Gets or create the 'Sale Order' for this project.
    """

    def getSaleOrder(self, auto_create=True):

        result = self.sale_order_id
        if not result and auto_create:
            self.sale_order_id = self.env['sale.order'].create(
                [{'partner_id': self.partner_id.id}]
                #[{'project_id': self._project_attribute_name}]
            )
        return result

    """
        Adds a product to project. The porduct is actually added
        to the sale order.
        Before adding the product, a project variant is created.

    """

    def addProduct(self, product_tmpl_id: HvacProductTemplateExtensions, bom_id: HvacMrpBomExtensions):
        result = False
        utils = self.getUtils()
        utils.getProjectAttributeValue(self.code)
        product_id = product_tmpl_id.getProjectVariant(self)

        # utils.ensureProjectAttributeIsSelectedOnProductTemplate(
        #     product_tmpl_id, self.code)
        # product_id:HvacProductExtensions = utils.createProjectProductVariant(
        #     product_tmpl_id, self.code)
        
        if bom_id:
            bom_id.fork(self)
        sale_order = self.getSaleOrder(True)
        sale_order_line = self.env['sale.order.line'].create([{
            'order_id': sale_order.id,
            'product_template_id': product_tmpl_id.id,
            'product_id': product_id.id
        }])
        return result

    def test(self):
        for line in self.sale_order_lines:
            product = line.product_template_id
            print(product.name)
            for bom_id in product.bom_ids:
                print(bom_id.display_name)
                for bom_line in bom_id.bom_line_ids:
                    name = bom_line.id
        print('here')

    # def addProduct(self):
    #     utils = self.env["hvac.utils"]
    #     p = "test"
    #     utils.test()
    #     #gg = p.product_template_attribute_value_ids
    #     #variant = p.product_template_attribute_value_ids._get_combination_name()
    #     # for attribute_value in p.mapped('attribute_line_ids.value_ids'):
    #     #     print(attribute_value)
    #     # vv = p.valid_product_template_attribute_line_ids
    #     print("here")

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'hvac.mrp.project') or 'New'
        # res = super(Class_Name, self).create(vals)
        # vals['code'] = 'test'
        result = super(HvacMrpProject, self).create(vals)
        return result

    @api.model
    def _default_code(self):
        seq_date = None

        result = self.env['ir.sequence'].next_by_code(
            'hvac.mrp.project', sequence_date=seq_date)
        # print("hey")
        # print(result)
        #result = "P_001"
        return result

    @api.depends('sale_order_id')
    def _compute_sale_order_lines(self):
        for record in self:
            record.sale_order_lines = record.sale_order_id.order_line
            # reconciled_moves = record.move_line_ids.mapped('matched_debit_ids.debit_move_id.move_id')\
            #                    + record.move_line_ids.mapped('matched_credit_ids.credit_move_id.move_id')
            # record.reconciled_invoice_ids = reconciled_moves.filtered(lambda move: move.is_invoice())
            # record.has_invoices = bool(record.reconciled_invoice_ids)
            # record.reconciled_invoices_count = len(record.reconciled_invoice_ids)


class HvacMrpProduction(models.Model):

    _inherit = 'mrp.production'
    project_id = fields.Many2one('hvac.mrp.project', "mf_order")


class HvacProductionTasks(models.Model):
    _name = "hvac.mrp.tasks"

    name = fields.Char()
    mrp_ref = fields.Many2one("hvac.mrp.project", 'task_ids')
    manufacturing_order = fields.Many2one('mrp.production')
    product_id = fields.Many2one('product.product')


# class HvacMrpProjectProductLine(models.Model):
#     _name = "hvac.mrp.project.product.line"
#     project_id = fields.Many2one("hvac.mrp.project")

#     product
