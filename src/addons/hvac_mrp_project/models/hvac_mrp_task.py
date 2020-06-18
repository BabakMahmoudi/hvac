from odoo import models, fields, api
from datetime import datetime
from datetime import timedelta
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from hvac_mrp_project.models.hvac_imports import \
        HvacProductExtensions, HvacProductTemplateExtensions, HvacUtils, \
        HvacMrpBomExtensions, HvacMrpBomLineExtensions, HvacSaleOrderLineExtensions, \
        HvacSaleOrderExtensions, HvacStockMove, HvacStockMoveLine, HvacMrpProduction, \
        HvacPurchaseOrderLine, HvacPurchaseOrder, RecalculateProjectWizard, \
        ReviseProjectWizard, HvacMrpProject
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
    RecalculateProjectWizard = models.Model
    ReviseProjectWizard = models.Model
    HvacMrpProject = models.Model


class HvacMrpTask(models.Model):
    _name = 'hvac.mrp.task'
    _order = "sequence, start"
    name = fields.Char()
    active = fields.Boolean(default=True)
    project_id = fields.Many2one("hvac.mrp.project")
    sequence = fields.Integer(string='Sequence', default=10)
    TYPE_MO = 'MO'
    TYPE_PO = 'PO'
    TYPE_EN = 'EN'
    TYPE_LO = 'LO'
    TYPE_OT = 'OT'
    task_type = fields.Selection(
        [(TYPE_MO, 'Manufacturing'), (TYPE_PO, 'Purchase'), (TYPE_EN, 'Engineering'),
         (TYPE_LO, 'Logistic'), (TYPE_OT, 'Other')],
        default='',
        String="Type")

    manufacturing_order = fields.Many2one('mrp.production')
    product_id = fields.Many2one('product.product')
    purchase = fields.Many2one("purchase.order.line")
    planned_start = fields.Datetime()
    planned_finish = fields.Datetime()
    start = fields.Datetime()
    finish = fields.Datetime()
    deadline = fields.Datetime()
    duration = fields.Float()
    responsible_id = fields.Many2one(
        'res.users', string='Responsible', default=lambda self: self.env.uid, company_dependent=True, check_company=True,
        help="This user will be responsible of the next activities related to logistic operations for this product.")
    parent_task = fields.Many2one('hvac.mrp.task')
    # successor_id = fields.Many2one('hvac.mrp.task')
    # predecessor_ids = fields.One2many('hvac.mrp.task','successor_id')
    successor_ids = fields.Many2many(
        'hvac.mrp.task', 'task_task_rel', 'successor_id', 'prdecessor_id')
    predecessor_ids = fields.Many2many(
        'hvac.mrp.task', 'task_task_rel', 'prdecessor_id', 'successor_id')

    def get_manufacturing_order(self) -> HvacMrpProduction:
        return self.manufacturing_order

    def get_task_for_purchase(self, PO: HvacPurchaseOrderLine, project):
        result = self.env[self._name].search([
            ('purchase', '=', PO.id), ('project_id', '=', project.id)])
        if not result:
            result = self.env[self._name].create({
                'purchase': PO.id,
                'project_id': project.id,
                # 'name' : PO.name

            })
        return result

    def get_task_for_production(self, MO: HvacMrpProduction, project):
        result = self.env[self._name].search([
            ('manufacturing_order', '=', MO.id), ('project_id', '=', project.id)])
        if not result:
            result = self.env[self._name].create({
                'manufacturing_order': MO.id,
                'project_id': project.id,
                'planned_start': MO.date_planned_start,
                'planned_finish': MO.date_planned_finished,
                # 'name' : 'manufacture : {}'.format(MO.name)
            })
        return result

    def get_default_name(self):
        res = ''
        if self.manufacturing_order:
            res = 'Manufacture {}'.format(
                self.get_manufacturing_order().product_tmpl_id.name)
        if self.purchase:
            res = 'Purchase {}'.format(self.purchase.name)
        return res

    def get_default_task_type(self):
        if self.manufacturing_order:
            return self.TYPE_MO
        if self.purchase:
            return self.TYPE_PO
        return self.TYPE_OT

    def get_purchase_oder_line(self) -> HvacPurchaseOrderLine:
        return self.purchase

    def get_project(self) -> HvacMrpProject:
        return self.project_id

    def get_planned_start(self, recompute=True):
        res = self.planned_start
        if not res and recompute:
            mo: HvacMrpProduction = self.manufacturing_order
            if mo:
                res = mo.date_planned_start
            if not res:
                res = self.get_project().get_planned_start_date()
        return res

    def get_finish_date(self, recompute=True):
        res = self.finish
        if not res and recompute:
            mo: HvacMrpProduction = self.manufacturing_order
            if mo:
                res = mo.date_planned_finished
            if not res:
                res = self.get_project().get_finish_date()
        return res
    
    def get_expected_duration(self, recompute=True):
        res = self.duration
        if not res and recompute:
            mo: HvacMrpProduction = self.manufacturing_order
            if mo:
                res = (mo.date_planned_finished - mo.date_planned_start).total_seconds()/86400
            if not res or res<.5:
                res = 1
        return res

    def get_start(self, recompute=True):
        res = self.start
        if not res and recompute:
            mo: HvacMrpProduction = self.manufacturing_order
            if mo:
                res = mo.date_planned_start
            if not res and self.get_purchase_oder_line():
                res = self.get_purchase_oder_line().date_order
            if not res:
                res = self.get_project().get_start_date()
        return res

    def get_latest_predecessor(self):
        latest = self.predecessor_ids.sorted(lambda x: x.finish, True)
        if latest and len(latest) > 0 and latest[0].id != self.id:
            return latest[0]
        return False

    def reschedule(self, opt: ReviseProjectWizard):
        _predecessor = self.get_latest_predecessor()
        if not self.start or not self.finish:
            return self
        # _dur = self.get_expected_duration()
        _dur = self.finish - self.start
        if _predecessor:
            if self.start < (_predecessor.finish + timedelta(days=1)):
                self.start = _predecessor.finish + timedelta(days=1)
                self.finish = self.start + _dur

        return self


    def revise(self, options: ReviseProjectWizard):
        """
            Revises and recalculates a task based on options.
        """
        proj: HvacMrpProject = self.project_id

        def should_be_canceled():
            res = False
            if self.get_manufacturing_order() and self.get_manufacturing_order().is_canceled():
                res = True
            return res

        def revise_name():
            _name = self.get_default_name()
            if self.name == '' or self.name != _name:
                self.name = _name
            return True

        def revise_dates():
            _start = self.get_start()
            _finish = self.get_finish_date()
            _duration = self.get_expected_duration()
            if _duration< (_finish-_start).total_seconds()/86400:
                _duration = (_finish-_start).total_seconds()/86400

            _planned_start = self.planned_start
            _planned_finish = self.planned_finish
            # _start = self.compute_start_date()
            # if options.reschedule:
            #     _start = self.compute_start_date()
            #     _finish = self.compute_finish_date()
            # predecessor = get_latest_predecessor()
            # if predecessor:
            #     _start = predecessor.finish
            if _finish < _start + timedelta(days=_duration):
                _finish = _start+timedelta(days=_duration)
            if not self.duration or self.duration!= _duration:
                self.duration = _duration
            if not _planned_start or options.replan:
                _planned_start = _start
            if not _planned_finish or options.replan:
                _planned_finish = _finish
            if not self.start or self.start != _start:
                self.start = _start
            if not self.finish or self.finish != _finish:
                self.finish = _finish
            if not self.planned_start or self.planned_start != _planned_start:
                self.planned_start = _planned_start
            if not self.planned_finish or self.planned_finish != _planned_finish:
                self.planned_finish = _planned_finish
            return True

        def revise_product():
            if not self.product_id:
                if self.get_manufacturing_order():
                    self.product_id = self.get_manufacturing_order().product_id
                if not self.product_id and self.get_purchase_oder_line():
                    self.product_id = self.get_purchase_oder_line().product_id
            return True

        # revise task dates
        to_be_canceled = should_be_canceled()
        if not to_be_canceled:
            self.parent_task = self
            revise_product()
            revise_name()
            revise_dates()
            # if self.get_purchase_oder_line():
            #     self.successor_ids = self.successor_ids.concat(self.get_project().task_ids[0])
        else:
            self.active = False
        return self

    def recalculate(self, options: RecalculateProjectWizard):

        self.task_type = self.get_default_task_type()
        self.name = self.get_default_name()
        self.parent_task = self

        return self


# class HvacMrpProjectProductLine(models.Model):
#     _name = "hvac.mrp.project.product.line"
#     project_id = fields.Many2one("hvac.mrp.project")

#     product
