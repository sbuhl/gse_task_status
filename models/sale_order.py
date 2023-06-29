# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    task_status = fields.Selection([
        ('in progress', 'In Progress'),
        ('partially finished', 'Partially Finished'),
        ('finished', 'Finished'),
    ], string='Task Status', compute='_compute_tasks_ids', compute_sudo=False, store=True)

    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)

    mo_value = fields.Monetary(compute='_compute_mo_value', string='MO Value')
    mo_value_technician = fields.Monetary(compute='_compute_mo_value_technician', string='MO Value Technician')
    mo_technicians = fields.Many2many('res.users', string='MO Technicians', compute='_compute_mo_technicians', store=True)

    @api.depends('tasks_ids.user_ids')
    def _compute_mo_technicians(self):
        for order in self:
            order.mo_technicians = order.tasks_ids.mapped('user_ids')
    
    @api.depends('order_line.product_id.service_tracking')
    def _compute_mo_value(self):
        for order in self:
            order.mo_value = sum(order.order_line.filtered(lambda l: l.product_id.service_tracking == 'task_global_project').mapped('price_subtotal'))

    @api.depends('mo_value')
    def _compute_mo_value_technician(self):
        for order in self:
            order.mo_value_technician = order.mo_value * 0.1
    
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