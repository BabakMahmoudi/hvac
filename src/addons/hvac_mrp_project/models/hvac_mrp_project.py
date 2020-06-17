from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from hvac_mrp_project.models.hvac_imports import \
        HvacProductExtensions, HvacProductTemplateExtensions, HvacUtils, \
        HvacMrpBomExtensions, HvacMrpBomLineExtensions, HvacSaleOrderLineExtensions, \
        HvacSaleOrderExtensions, HvacStockMove, HvacStockMoveLine, HvacMrpProduction, \
        HvacPurchaseOrderLine, HvacPurchaseOrder, HvacMrpTask
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
    HvacSaleOrderLineExtensions = models.Model
    HvacSaleOrderExtensions = models.Model
    HvacStockMove = models.Model
    HvacStockMoveLine = models.Model
    HvacMrpProduction = models.Model
    HvacPurchaseOrderLine = models.Model
    HvacPurchaseOrder = models.Model
    HvacMrpTask = models.Model


class HvacMrpProject(models.Model):
    _name = "hvac.mrp.project"
    _description = 'Manufacturing Project'
    numbers = [1, 2, 3]
    name = fields.Char("Name")
    code = fields.Char(string='Code', required=True, copy=False, readonly=False,
                       index=True,
                       default=lambda self: self._default_code()
                       )

    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=False,
        #states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        #domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    sale_order_lines = fields.One2many(
        'sale.order.line', compute='_compute_sale_order_lines', readonly=True)

    task_ids = fields.One2many('hvac.mrp.task', 'project_id')
    bom_id = fields.Many2one('mrp.bom', "Bill of Materials")
    sale_order_id = fields.Many2one('sale.order')
    deliverable_product_id = fields.Many2one(
        'product.product', string="Deliverable",
        #default=lambda self: self._default_deliverable_product_id(),
        readonly=False,)

    def test(self):
        # product: HvacProductTemplateExtensions = self.env['product.template'].search(
        #     [('name', '=', 'Assembly 1')])
        # product.ensureProject(self)

        self.getProjectBom(recreate=True)
        # self.getSaleOrder().action_confirm()
        #sale_order = self.getSaleOrder()
        self.Recalculate()
        # for _line in sale_order.order_line:
        #     line: HvacSaleOrderLineExtensions = _line
        #     line.move_ids

        return False

    @api.onchange('code')
    def _on_code_changed(self):
        self.deliverable_product_id = self.getProjectDeliverableProduct()
        self.name = self.code
        return False

    def get_numbers(self):
        return [1, 2, 3]

    def getUtils(self) -> HvacUtils:
        return self.env['hvac.utils']

    @api.model
    def _default_deliverable_product_id(self):
        return self.getProjectDeliverableProduct()

    def get_suitable_product_bom(self, product: HvacProductExtensions, sale_order_line: HvacSaleOrderLineExtensions, ) -> HvacMrpBomExtensions:
        result = False
        if sale_order_line:
            result = sale_order_line.bom_id
        if not result and product:
            result = product.get_best_bom_for_forking(self)

        return result

    def create_project_bom(self, product: HvacProductExtensions) -> HvacMrpBomExtensions:
        if not product:
            product = self.getProjectDeliverableProduct()
        result = self.env['mrp.bom'].create({
            'product_id': product.id,
            'product_tmpl_id': product.product_tmpl_id.id,
            # 'product_tmpl_id': self.product_7_template.id,
            'product_uom_id': product.uom_id.id,
            'product_qty': 1.0,
            # 'routing_id': self.routing_2.id,
            'type': 'normal',
        })
        for _l in self.sale_order_lines:
            l: HvacSaleOrderLineExtensions = _l
            self.env['mrp.bom.line'].create({
                'bom_id': result.id,
                'product_id': l.product_id.id,
                'product_qty': l.product_uom_qty,
                'child_bom_id': self.get_suitable_product_bom(l.product_id, l)
            })
        return result
        # test_bom_l2 = self.env['mrp.bom.line'].create({
        #     'bom_id': test_bom.id,
        #     'product_id': self.product_3.id,
        #     'product_qty': 2,
        #     'bom_product_template_attribute_value_ids': [(4, self.product_7_attr1_v1.id)],
        # })
        # test_bom_l3 = self.env['mrp.bom.line'].create({
        #     'bom_id': test_bom.id,
        #     'product_id': self.product_4.id,
        #     'product_qty': 2,
        #     'bom_product_template_attribute_value_ids': [(4, self.product_7_attr1_v2.id)],
        # })

    def getProjectDeliverableProduct(self, auto_create=True) -> HvacProductExtensions:
        """
            Gets or creates a virtual product for the project
            deliverable (output). This is used to assign a grand bill
            of material to the whole project.
        """
        result: HvacProductExtensions = self.deliverable_product_id
        if not result and auto_create:
            self.deliverable_product_id = self.env['product.product'].create([
                {
                    # 'Deliveravle' #+ (self.code if self.code else "XXXX")
                    'name': self.code,
                    'sale_ok': False
                }])
            p: HvacProductExtensions = self.deliverable_product_id

        return self.deliverable_product_id

    def getProjectBom(self, auto_create=True, recreate=False) -> HvacMrpBomExtensions:
        """
            Gets a grand bill of materials for the totality of project as a virtual 
            BOM assigned to the project virtual deliverable product.

        """
        result = self.bom_id
        if (not result and auto_create) or recreate:
            product = self.getProjectDeliverableProduct(auto_create)
            self.bom_id = self.create_project_bom(product)
        return self.bom_id

    def getSaleOrder(self, auto_create=True) -> HvacSaleOrderExtensions:
        """
            Gets or create the 'Sale Order' for this project.
        """
        result = self.sale_order_id
        if not result and auto_create:
            self.sale_order_id = self.env['sale.order'].create(
                [{
                    'partner_id': self.partner_id.id,
                    'project_id': self.id
                }]
                #[{'project_id': self._project_attribute_name}]
            )
        return result

    def get_product_used_count(self, product_tmpl_id: HvacProductTemplateExtensions):
        res = self.sale_order_lines.filtered(
            lambda x: x.product_template_id.id == product_tmpl_id.id)
        return len(res)

    def onSaleOrderStatusChanged(self, saleoder: HvacSaleOrderExtensions, new_state: str):
        """
            This method is called from SaleOrder when the state of the 
            sale order is changed.
        """
        print("SalerOrder State Changed: {}".format(new_state))
        pass

    def getTasks(self) -> HvacMrpTask:
        return self.task_ids

    def Recalculate(self):
        """
            Recalculates the project.
        """
        def get_moves() -> List[HvacStockMove]:
            res = []
            sale_order = self.getSaleOrder()
            if sale_order:
                for l in sale_order.order_line:
                    line: HvacSaleOrderLineExtensions = l
                    for m in line.move_ids:
                        res.append(m)
            return res

        def process_production(production: HvacMrpProduction):
            if production:
                print('MO for {0}'.format(production.product_id.display_name))
                task: HvacMrpTask = self.task_ids.get_task_for_production(
                    production, self)
                

                for move in production.getRawComponentsMove():
                    process_move(move)
            return False

        def process_purchase(purchase_line: HvacPurchaseOrderLine):
            if purchase_line:
                print('Purchase Line: {}'.format(purchase_line.name))
                self.task_ids.get_task_for_purchase(purchase_line, self)
            return True

        def process_move(move: HvacStockMove):
            production = move.getCreatedProduction()
            purchase_line = move.getCreatedPurchaseLine()
            if production:
                process_production(production)
            if purchase_line:
                process_purchase(purchase_line)
            # process this production

            return False
        for move in get_moves():
            process_move(move)
            # production = move.getCreatedProduction()
            # print(production.ids)

        return False

    def addProduct(self, product_tmpl_id: HvacProductTemplateExtensions, bom_id: HvacMrpBomExtensions):
        """
            Adds a product to project. The porduct is actually added
            to the sale order.
            Before adding the product, a project variant is created.

        """
        result = False

        count = self.get_product_used_count(product_tmpl_id)
        section = '{}'.format(count)
        utils = self.getUtils()
        product_tmpl_id.ensureProject(self, section=section)
        product = product_tmpl_id.getProjectVariant(self, section=section)
        product.get_boms()
        # utils.createProjectProductVariant(
        #     product_tmpl_id, self.code)
        if bom_id:
            for line in bom_id.bom_line_ids:
                a: HvacMrpBomLineExtensions = line
                a.product_tmpl_id.getProjectVariant(self, section)
        # self.flush()
        product_tmpl_id.fork(self, bom_id, section=section)
        bom = False
        boms = product.get_boms()
        bom = boms[0] if boms and len(boms) > 0 else bom_id
        sale_order = self.getSaleOrder(True)
        self.env['sale.order.line'].create([{
            'order_id': sale_order.id,
            'product_template_id': product_tmpl_id.id,
            'product_id': product.id,
            'bom_id': bom.id if bom else False
        }])
        return result

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'hvac.mrp.project') or 'New'
        result = super(HvacMrpProject, self).create(vals)
        return result

    @api.model
    def default_get(self, fields_list):
        defaults = super(HvacMrpProject, self).default_get(fields_list)
        #defaults['name'] = 'babak'

        # if self.env.context.get('default_raw_material_production_id'):
        #     production_id = self.env['mrp.production'].browse(self.env.context['default_raw_material_production_id'])
        #     if production_id.state == 'done':
        #         defaults['state'] = 'done'
        #         defaults['product_uom_qty'] = 0.0
        #         defaults['additional'] = True
        return defaults

    @api.model
    def _default_code(self):
        seq_date = None

        result = self.env['ir.sequence'].next_by_code(
            'hvac.mrp.project', sequence_date=seq_date)
        #self._auto_code = result
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

