# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    task_status = fields.Selection([
        ('in progress', 'In Progress'),
        ('partially finished', 'Partially Finished'),
        ('finished', 'Finished'),
    ], string='Task Status', compute='_compute_task_status', compute_sudo=False, store=True)

    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', copy=True)

    mo_value = fields.Monetary(compute='_compute_mo_value', string='MO Value')
    mo_value_technician = fields.Monetary(compute='_compute_mo_value_technician', string='MO Value Technician',store=True)
    mo_technicians = fields.Many2many('res.users', string='MO Technicians', compute='_compute_mo_technicians')

    tasks_ids = fields.Many2many('project.task', string='Tasks For Status', search='_search_tasks_ids')

    @api.depends('tasks_ids', 'tasks_ids.user_ids')
    def _compute_mo_technicians(self):
        for order in self:
            order.mo_technicians = order.tasks_ids.mapped('user_ids')

    @api.depends('order_line.price_subtotal', 'order_line.product_id.service_tracking')
    def _compute_mo_value(self):
        for order in self:
            order.mo_value = sum(
                line.price_subtotal
                for line in order.order_line
                if line.product_id.service_tracking == 'task_global_project'
            )

    @api.depends('mo_value')
    def _compute_mo_value_technician(self):
        for order in self:
            order.mo_value_technician = order.mo_value * 0.1 if order.mo_value else 0.0

    @api.depends('order_line.product_id.project_id')
    def _compute_task_status(self):
        for order in self:
            is_closed = order.state in ["1_done", "1_canceled"]
            if not order.tasks_ids:
                order.task_status = False
            elif all(is_closed is True for p in order.tasks_ids):
                order.task_status = 'finished'
            elif any(is_closed is True for p in order.tasks_ids):
                order.task_status = 'partially finished'
            else:
                order.task_status = 'in progress'
