# -*- coding: utf-8 -*-

from odoo import models, fields


class Users(models.Model):
    _name = 'res.users'
    _inherit = [
        'res.users',
        'mail.thread',
    ]

    tasks_from_so_ids = fields.Many2many('project.task', relation='project_task_user_rel', column1='user_id', column2='task_id', string='Tasks For Status', domain="[('sale_order_id', '!=', None)]")
