# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    task_status = fields.Selection([
        ('in progress', 'In Progress'),
        ('partially finished', 'Partially Finished'),
        ('finished', 'Finished'),
    ], string='Task Status', compute='_compute_task_status', store=True)

    @api.depends('tasks_ids', 'tasks_ids.stage_id', 'tasks_ids.is_closed')
    def _compute_task_status(self):
        for order in self:
            if not order.tasks_ids:
                order.task_status = False
            elif all(p.is_closed is True for p in order.tasks_ids):
                order.task_status = 'finished'
            elif any(p.is_closed is True for p in order.tasks_ids):
                order.task_status = 'partially finished'
            else:
                order.task_status = 'in progress'
