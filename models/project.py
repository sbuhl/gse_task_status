# -*- coding: utf-8 -*-

from odoo import models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def write(self, vals):
        res = super().write(vals)
        if 'user_ids' in vals:
            self.clear_caches()
        return res
