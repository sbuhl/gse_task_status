# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    task_status = fields.Selection([
        ('in progress', 'In Progress'),
        ('partially finished', 'Partially Finished'),
        ('finished', 'Finished'),
    ], string='Task Status', compute='_compute_tasks_ids', store=True)

    @api.depends('order_line.product_id.project_id')
    def _compute_tasks_ids(self):
        # We need to do this in an overide as it depends of task_ids which is
        # itself a computed field -> It can't be added as @api.depends
        super()._compute_tasks_ids()
        for order in self:
            if not order.tasks_ids:
                order.task_status = False
            elif all(p.is_closed is True for p in order.tasks_ids):
                order.task_status = 'finished'
            elif any(p.is_closed is True for p in order.tasks_ids):
                order.task_status = 'partially finished'
            else:
                order.task_status = 'in progress'
