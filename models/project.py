# -*- coding: utf-8 -*-

from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = "project.task"

    mo_value_technician = fields.Many2one('sale.order', 'MO Value Technician', readonly=True, auto_join=True, index=True)
    
    def write(self, vals):
        res = super().write(vals)
        if 'user_ids' in vals:
            self.clear_caches()
        return res
        
