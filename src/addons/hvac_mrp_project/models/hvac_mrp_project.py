from odoo import models, fields, api
from datetime import datetime
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from hvac_mrp_project.models.hvac_imports import \
        HvacProductExtensions, HvacProductTemplateExtensions, HvacUtils, \
        HvacMrpBomExtensions, HvacMrpBomLineExtensions, HvacSaleOrderLineExtensions, \
        HvacSaleOrderExtensions, HvacStockMove, HvacStockMoveLine, HvacMrpProduction, \
        HvacPurchaseOrderLine, HvacPurchaseOrder, HvacMrpTask, RecalculateProjectWizard, \
        ReviseProjectWizard
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
    RecalculateProjectWizard = models.Model
    ReviseProjectWizard = models.Model


class HvacMrpProject(models.Model):
    _name = "hvac.mrp.project"
    _description = 'Manufacturing Project'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
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

    test_pct = fields.Integer(default=5)
    test_max = fields.Integer(default=100)

    sale_order_lines = fields.One2many(
        'sale.order.line', compute='_compute_sale_order_lines', readonly=True)

    task_ids = fields.One2many('hvac.mrp.task', 'project_id')
    bom_id = fields.Many2one('mrp.bom', "Bill of Materials")
    sale_order_id = fields.Many2one('sale.order')
    deliverable_product_id = fields.Many2one(
        'product.product', string="Deliverable",
        #default=lambda self: self._default_deliverable_product_id(),
        readonly=False,)
    planned_start = fields.Datetime()
    planned_finish = fields.Datetime()
    start = fields.Datetime()
    finish = fields.Datetime()
    deadline = fields.Datetime()
    percent_complete = fields.Integer(
        default=0,
    )
    planned_percent_complete = fields.Integer(

    )
    price = fields.Float()
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
        ('cancel' , "Cancel")

    ], default='draft')

    def action_draft(self):
        self.state = 'draft'
        sale_order = self.getSaleOrder().copy()
        self.getSaleOrder().action_cancel()
        self.sale_order_id = sale_order
          
    def action_confirm(self):
        self.state = 'confirmed'
        self.getSaleOrder().action_confirm()
        self.message_post(body="I Did this")
        
  
    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'
        self.getSaleOrder().action_cancel()


    def revise(self, opt: ReviseProjectWizard):
        def get_moves() -> List[HvacStockMove]:
            res = []
            sale_order = self.getSaleOrder()
            if sale_order:
                for l in sale_order.order_line:
                    line: HvacSaleOrderLineExtensions = l
                    for m in line.move_ids:
                        res.append(m)
            return res

        def process_production(production: HvacMrpProduction, stock_move):
            task = False
            if production:
                if opt.revise_sale_order:
                    production._action_cancel()
                task: HvacMrpTask = self.task_ids.get_task_for_production(
                    production, self, stock_move)
                task.revise(opt)
                for move in production.getRawComponentsMove():
                    move_task = process_move(move)
                    if move_task:
                        if not task.id in move_task.successor_ids.ids:
                            move_task.successor_ids = move_task.successor_ids.concat(
                                task)
            return task

        def process_purchase(purchase_line: HvacPurchaseOrderLine, stock_move):
            task = False
            if purchase_line:
                task: HvacMrpTask = self.task_ids.get_task_for_purchase(
                    purchase_line, self, stock_move)
                task.revise(opt)

            return task

        def process_move(move: HvacStockMove):
            production = move.getCreatedProduction()
            purchase_line = move.getCreatedPurchaseLine()

            res: HvacMrpTask = False
            if production:
                res = process_production(production, move)
            if purchase_line:
                res = process_purchase(purchase_line, move)
            # process this production

            return res

        def revise_dates():
            self.planned_start = self.get_planned_start_date()
            self.planned_finish = self.get_planned_finish_date()
            self.start = self.get_start_date()
            self.finish = self.get_finish_date()
            self.deadline = self.get_deadline__date()

            return self

        def reorder_by_date():
            try:
                sorted = self.task_ids.sorted(lambda x: x.start)
                i = 1
                for t in sorted:
                    t.sequence = i * 10
                    i = i + 1
            except:
                pass
            return True

        def product_id_in_sale_oder_lines(product_id):

            for l in self.sale_order_lines:
                if l.product_id.id==product_id:
                    return True


            return False
        def update_price():
            total = 0.0
            tasks = self.task_ids.sorted(lambda x: len(x.predecessor_ids))
            for _task in tasks:
                task: HvacMrpTask = _task
                task.update_price(opt)
                if task.product_id and product_id_in_sale_oder_lines(task.product_id.id):
                    total = total+task.price
                #total = total+task.price

            self.price = total
            return self

        def update_progress():
            tasks = self.task_ids.sorted(lambda x: len(x.predecessor_ids))
            total = 0
            total_price = 0

            for _task in tasks:
                task: HvacMrpTask = _task
                task.update_progress(opt)
                if task.product_id and product_id_in_sale_oder_lines(task.product_id.id):
                    total_price = total_price+task.price
                    total = total + task.percent_complete * task.price
            pct = 0
            if total_price > 0:
                pct = total/total_price

            self.percent_complete = pct
            return self

        revise_dates()
        revise_sale_oder = opt.revise_sale_order
        bom: HvacMrpBomExtensions = self.getProjectBom(recreate=False)
        if opt.revise_bom:
            bom = bom.revise(forced=True)
            self.bom_id = bom
        sale_oder = self.sale_order_id
        if sale_oder and revise_sale_oder:
            sale_oder = self.sale_order_id.copy()
            self.sale_order_id.state = 'cancel'
        for move in get_moves():
            process_move(move)
        if sale_oder:
            self.sale_order_id = sale_oder

        if opt.update_progress or not self.price:
            update_price()

        if opt.update_progress:
            update_progress()

        if True or opt.reschedule:
            tasks = self.task_ids.sorted(lambda x: len(x.predecessor_ids))
            for _task in tasks:
                task: HvacMrpTask = _task
                task.recalculate(opt)

        if opt.reschedule:
            tasks = self.task_ids.sorted(lambda x: len(x.predecessor_ids))
            for _task in tasks:
                task: HvacMrpTask = _task
                task.reschedule(opt)

        reorder_by_date()

        return self

    def test(self):
        # product: HvacProductTemplateExtensions = self.env['product.template'].search(
        #     [('name', '=', 'Assembly 1')])
        # product.ensureProject(self)

        bom: HvacMrpBomExtensions = self.getProjectBom(recreate=False)
        revised_bom = bom.revise(forced=True)
        self.bom_id = revised_bom
        new_sale = self.sale_order_id.copy()
        self.sale_order_id.state = 'cancel'
        self.sale_order_id = new_sale
        # if (bom.state=='draft'):
        #     bom.state='confirmed'
        # else:
        #     bom.revise()
        # self.getSaleOrder().action_confirm()
        #sale_order = self.getSaleOrder()
        # self.Recalculate()
        # for _line in sale_order.order_line:
        #     line: HvacSaleOrderLineExtensions = _line
        #     line.move_ids

        return False

    def get_deadline__date(self, recompute=True):
        res = self.deadline
        if not res and recompute:
            s: HvacSaleOrderExtensions = self.sale_order_id
            if s:
                res = s.date_order
        if not res and recompute:
            res = datetime.today()
        return res

    def get_planned_start_date(self, recompute=True):
        res = self.planned_start
        if not res and recompute:
            s: HvacSaleOrderExtensions = self.sale_order_id
            if s:
                res = s.date_order
        if not res and recompute:
            res = datetime.today()
        return res

    def get_planned_finish_date(self, recompute=True):
        res = self.planned_finish
        if not res and recompute:
            s: HvacSaleOrderExtensions = self.sale_order_id
            if s:
                res = s.date_order
        if not res and recompute:
            res = datetime.today()
        return res

    def get_start_date(self, recompute=True):
        res = self.start
        if not self.start and recompute:
            res = self.get_planned_start_date()
        return res

    def get_finish_date(self, recompute=True):
        res = self.finish
        if not res and recompute:
            res = self.get_planned_finish_date()
        return res

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

    def Recalculate(self, options: RecalculateProjectWizard = False):
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
                task.recalculate_deprecated(options)

                for move in production.getRawComponentsMove():
                    process_move(move)
            return False

        def process_purchase(purchase_line: HvacPurchaseOrderLine):
            if purchase_line:
                print('Purchase Line: {}'.format(purchase_line.name))
                task: HvacMrpTask = self.task_ids.get_task_for_purchase(
                    purchase_line, self)
                task.recalculate_deprecated(options)

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

        if not options:
            options = self.env['hvac.mrp.project.recalculate.project.wizard'].create([
            ])
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
