# -*- coding: utf-8 -*-

from odoo import api, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    def after_save(self):
        users = self.env['res.users'].search([])
        for user in users:
            user._compute_task_ids()   

    def write(self, vals):
        result = super(ProjectTask, self).write(vals)
        self.after_save()
        return result
    
    