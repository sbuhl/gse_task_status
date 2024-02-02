# -*- coding: utf-8 -*-

from odoo import models, fields,api


class Users(models.Model):
    _name = 'res.users'
    _inherit = [
        'res.users',
        'mail.thread',
    ]

    stored_sale_orders = fields.Many2many(
        'sale.order',
        'bk_sale_order_user_rel',
        'user_id',
        'sale_order_id',
        string='Sale Orders')
    tasks_ids = fields.Many2many('project.task', string='Tasks For Status', compute='_compute_task_ids')
    
    @api.depends('tasks_ids')
    def _compute_task_ids(self):
        for user in self:
            tasks = self.env['project.task'].search([])
            origin = user.id if user.id else user.id.origin
            assigned_tasks = tasks.filtered(lambda task: origin in task.user_ids.ids and task.sale_order_id) 
            user.tasks_ids = [(6, 0, assigned_tasks.ids)] 
            sale_order_ids = set(task.sale_order_id.id for task in user.tasks_ids) 
            user.stored_sale_orders = [(6, 0, list(sale_order_ids))]
            
